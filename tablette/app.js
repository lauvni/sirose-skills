/* Tablette Sir'Ose — ES5 strict, cible Chrome 81 / Android 4.4. Aucune dépendance. */
(function () {
  'use strict';

  var CLE_PIN = 'sirose_pin';
  var URL_DONNEES = 'data.enc';
  var S = {};
  window.SIROSE = S;

  function $(id) { return document.getElementById(id); }

  function lirePin() {
    try { return window.localStorage.getItem(CLE_PIN); } catch (e) { return null; }
  }
  function ecrirePin(pin) {
    try { window.localStorage.setItem(CLE_PIN, pin); } catch (e) { /* stockage indisponible : on redemandera */ }
  }
  function oublierPin() {
    try { window.localStorage.removeItem(CLE_PIN); } catch (e) { /* rien */ }
  }

  function b64VersOctets(b64) {
    var bin = window.atob(b64);
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) { out[i] = bin.charCodeAt(i); }
    return out;
  }

  function utf8(texte) {
    return new TextEncoder().encode(texte);
  }

  /* Déchiffre l'enveloppe {v, iter, sel, iv, ct}. ok(objet) ou ko('pin' | 'format'). */
  function enveloppeValide(env) {
    return !!env && env.v === 1 && typeof env.iter === 'number' &&
      typeof env.sel === 'string' && typeof env.iv === 'string' && typeof env.ct === 'string';
  }

  S.dechiffrer = function (env, pin, ok, ko) {
    var subtle = window.crypto && window.crypto.subtle;
    if (!subtle) { ko('crypto'); return; }
    if (!enveloppeValide(env)) { ko('format'); return; }
    var sel, iv, ct;
    try { sel = b64VersOctets(env.sel); iv = b64VersOctets(env.iv); ct = b64VersOctets(env.ct); } catch (e) { ko('format'); return; }
    subtle.importKey('raw', utf8(pin), { name: 'PBKDF2' }, false, ['deriveKey'])
      .then(function (base) {
        return subtle.deriveKey(
          { name: 'PBKDF2', hash: 'SHA-256', salt: sel, iterations: env.iter },
          base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (cle) {
        return subtle.decrypt({ name: 'AES-GCM', iv: iv }, cle, ct);
      })
      .then(function (clair) {
        var objet;
        try { objet = JSON.parse(new TextDecoder('utf-8').decode(clair)); } catch (e) { ko('format'); return; }
        ok(objet);
      }, function () { ko('pin'); });
  };

  var compteur = 0;

  function charger(ok, ko) {
    var xhr = new XMLHttpRequest();
    compteur += 1;
    var fini = false;
    function echec() { if (!fini) { fini = true; ko('reseau'); } }
    xhr.open('GET', URL_DONNEES + '?t=' + new Date().getTime() + '-' + compteur, true);
    xhr.timeout = S.DELAI_RESEAU;
    xhr.ontimeout = echec;
    xhr.onreadystatechange = function () {
      if (xhr.readyState !== 4 || fini) { return; }
      if (xhr.status === 0) { return; } /* timeout ou coupure : géré par ontimeout / onerror */
      fini = true;
      if (xhr.status === 200) {
        var env;
        try { env = JSON.parse(xhr.responseText); } catch (e) { ko('reseau'); return; }
        ok(env);
      } else {
        ko('reseau');
      }
    };
    xhr.onerror = echec;
    xhr.send();
  }

  /* effacer : vide le champ (après un code refusé), jamais lors d'une relance automatique. */
  function montrerPin(message, effacer) {
    $('tableau').hidden = true;
    $('ecran-pin').hidden = false;
    $('message-pin').textContent = message || '';
    if (effacer) { $('champ-pin').value = ''; }
  }

  var relance = null;
  function planifierRelance() {
    if (relance) { window.clearTimeout(relance); }
    relance = window.setTimeout(function () { relance = null; S.rafraichir(); }, 60000);
  }

  var DECALAGE_REUNION = 4 * 3600 * 1000; /* UTC+4, pas d'heure d'été */
  var PERIME_APRES = 8 * 3600 * 1000;
  var RAFRAICHISSEMENT = 15 * 60 * 1000;
  S.DELAI_RESEAU = 30000;
  var JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
  var SOURCES = { gmail: 'G', notion: 'N', drive: 'D', registre: 'R' };
  var BLOCS = [
    { id: 'priorites', titre: 'Priorités du jour', max: 3 },
    { id: 'taches', titre: 'Tâches & échéances', max: 8 },
    { id: 'mails', titre: 'Mails à traiter', max: 8 },
    { id: 'pipeline', titre: 'Pipeline', max: 6 }
  ];

  function deux(n) { return (n < 10 ? '0' : '') + n; }

  /* Heure de La Réunion, quel que soit le fuseau de la tablette. */
  function reunion(ms) { return new Date(ms + DECALAGE_REUNION); }
  function hhmm(ms) { var r = reunion(ms); return deux(r.getUTCHours()) + ':' + deux(r.getUTCMinutes()); }
  function jjmm(ms) { var r = reunion(ms); return deux(r.getUTCDate()) + '/' + deux(r.getUTCMonth() + 1); }
  function iso(ms) { return Date.parse(ms); }

  function euros(n) {
    var entier = String(Math.round(n));
    var out = '';
    while (entier.length > 3) { out = ' ' + entier.slice(-3) + out; entier = entier.slice(0, -3); }
    return entier + out + ' €';
  }

  function el(tag, classe, texte) {
    var e = document.createElement(tag);
    if (classe) { e.className = classe; }
    if (texte !== undefined && texte !== null) { e.textContent = texte; }
    return e;
  }

  function vider(e) { while (e.firstChild) { e.removeChild(e.firstChild); } }

  function enteteBloc(conteneur, titre, bloc) {
    vider(conteneur);
    conteneur.appendChild(el('h2', null, titre));
    if (bloc && bloc.etat === 'indisponible') {
      var quand = bloc.depuis ? ' à ' + hhmm(iso(bloc.depuis)) : '';
      conteneur.appendChild(el('div', 'indispo', '⚠ source indisponible' + quand + ' — dernières données connues'));
    }
  }

  function rendreListe(def, bloc) {
    var c = $('bloc-' + def.id);
    enteteBloc(c, def.titre, bloc);
    var elements = (bloc && bloc.elements) || [];
    if (!elements.length) { c.appendChild(el('div', 'vide', 'Rien à signaler')); return; }
    var ul = el('ul');
    for (var i = 0; i < elements.length && i < def.max; i++) {
      var x = elements[i];
      var li = el('li', 'u-' + (x.urgence || 'basse'));
      li.appendChild(el('span', 'src', SOURCES[x.source] || '?'));
      li.appendChild(document.createTextNode(x.texte));
      if (x.lien_vers) { li.appendChild(el('span', 'lien', '↔ ' + x.lien_vers)); }
      if (x.echeance) {
        var p = x.echeance.split('-');
        li.appendChild(el('span', 'ech', '⏰ ' + p[2] + '/' + p[1]));
      }
      ul.appendChild(li);
    }
    c.appendChild(ul);
  }

  function ligneArgent(c, titre, v) {
    c.appendChild(el('div', 'sous', titre));
    c.appendChild(el('div', 'chiffre', euros(v.encaisse) + ' encaissés / ' + euros(v.objectif)));
    var barre = el('div', 'barre');
    var rempli = el('div');
    var pct = v.objectif > 0 ? Math.min(100, Math.round(100 * v.encaisse / v.objectif)) : 0;
    rempli.style.width = pct + '%';
    barre.appendChild(rempli);
    c.appendChild(barre);
    c.appendChild(el('div', 'sous', 'Facturé : ' + euros(v.facture) + ' · ' + pct + ' % de l\'objectif'));
  }

  function rendreArgent(bloc) {
    var c = $('bloc-argent');
    enteteBloc(c, 'Argent', bloc);
    if (!bloc || !bloc.mois) { c.appendChild(el('div', 'vide', 'Pas encore de données')); return; }
    ligneArgent(c, 'Mois de ' + bloc.mois.libelle, bloc.mois);
    if (bloc.phase) { ligneArgent(c, bloc.phase.nom + ' (cumul)', bloc.phase); }
  }

  function bandeau(texte) {
    var b = $('bandeau');
    b.textContent = texte || '';
    b.hidden = !texte;
  }

  function verifierFraicheur() {
    var d = S.derniere;
    if (!d) { return; }
    var genere = iso(d.genere_le);
    if (S.horsLigneDepuis) {
      bandeau('⚠ hors ligne depuis ' + hhmm(S.horsLigneDepuis) + ' — affichage des données du ' + jjmm(genere) + ' ' + hhmm(genere));
    } else if (Date.now() - genere > PERIME_APRES) {
      bandeau('⚠ données du ' + jjmm(genere) + ' ' + hhmm(genere) + ' — ARGOS n\'a pas mis à jour depuis plus de 8 h');
    } else {
      bandeau('');
    }
  }

  S.rendre = function (d) {
    var maintenant = reunion(Date.now());
    $('date-du-jour').textContent = JOURS[maintenant.getUTCDay()] + ' ' + maintenant.getUTCDate() + ' ' + MOIS[maintenant.getUTCMonth()];
    var h = 'màj ' + hhmm(iso(d.genere_le));
    if (d.prochaine_maj) { h += ' · prochaine ' + hhmm(iso(d.prochaine_maj)); }
    $('horodatage').textContent = h;
    var blocs = d.blocs || {};
    for (var i = 0; i < BLOCS.length; i++) { rendreListe(BLOCS[i], blocs[BLOCS[i].id]); }
    rendreArgent(blocs.argent);
    verifierFraicheur();
  };

  function afficher(d) {
    S.derniere = d;
    S.horsLigneDepuis = null;
    $('ecran-pin').hidden = true;
    $('tableau').hidden = false;
    S.rendre(d);
  }

  function ouvrir(pin) {
    charger(function (env) {
      S.dechiffrer(env, pin, function (d) {
        ecrirePin(pin);
        afficher(d);
      }, function (raison) {
        if (raison === 'pin') { oublierPin(); montrerPin('Code incorrect', true); }
        else if (raison === 'crypto') { montrerPin('HTTPS requis'); }
        else { montrerPin('Données illisibles'); planifierRelance(); }
      });
    }, function () {
      if (S.derniere) {
        if (!S.horsLigneDepuis) { S.horsLigneDepuis = Date.now(); }
        verifierFraicheur();
        return;
      }
      montrerPin('Hors ligne — nouvel essai dans 1 min');
      planifierRelance();
    });
  }

  S.demarrer = function () {
    $('bouton-pin').onclick = function () {
      var pin = $('champ-pin').value;
      if (pin) { $('message-pin').textContent = 'Ouverture…'; ouvrir(pin); }
    };
    $('champ-pin').onkeydown = function (e) { if (e.keyCode === 13) { $('bouton-pin').onclick(); } };
    var pin = lirePin();
    if (pin) { ouvrir(pin); } else { montrerPin('', true); }
    window.setInterval(S.rafraichir, RAFRAICHISSEMENT);
  };

  /* Recharge data.enc avec le PIN mémorisé ; en cas d'échec réseau, garde l'affichage. */
  S.rafraichir = function () {
    var pin = lirePin();
    if (pin) { ouvrir(pin); }
  };

  window.addEventListener('load', S.demarrer);
}());
