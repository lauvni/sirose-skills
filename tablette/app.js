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
  S.dechiffrer = function (env, pin, ok, ko) {
    var subtle = window.crypto && window.crypto.subtle;
    if (!subtle) { ko('crypto'); return; }
    subtle.importKey('raw', utf8(pin), { name: 'PBKDF2' }, false, ['deriveKey'])
      .then(function (base) {
        return subtle.deriveKey(
          { name: 'PBKDF2', hash: 'SHA-256', salt: b64VersOctets(env.sel), iterations: env.iter },
          base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (cle) {
        return subtle.decrypt({ name: 'AES-GCM', iv: b64VersOctets(env.iv) }, cle, b64VersOctets(env.ct));
      })
      .then(function (clair) {
        var objet;
        try { objet = JSON.parse(new TextDecoder('utf-8').decode(clair)); } catch (e) { ko('format'); return; }
        ok(objet);
      }, function () { ko('pin'); });
  };

  function charger(ok, ko) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', URL_DONNEES + '?t=' + new Date().getTime(), true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState !== 4) { return; }
      if (xhr.status === 200) {
        var env;
        try { env = JSON.parse(xhr.responseText); } catch (e) { ko('reseau'); return; }
        ok(env);
      } else {
        ko('reseau');
      }
    };
    xhr.send();
  }

  function montrerPin(message) {
    $('tableau').hidden = true;
    $('ecran-pin').hidden = false;
    $('message-pin').textContent = message || '';
    $('champ-pin').value = '';
  }

  S.rendre = function (d) {
    $('horodatage').textContent = 'màj ' + d.genere_le;
  };

  function afficher(d) {
    S.derniere = d;
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
        if (raison === 'pin') { oublierPin(); montrerPin('Code incorrect'); }
        else { montrerPin('Données illisibles'); }
      });
    }, function () {
      montrerPin('Hors ligne — nouvel essai dans 1 min');
      window.setTimeout(function () { var p = lirePin(); if (p) { ouvrir(p); } }, 60000);
    });
  }

  S.demarrer = function () {
    $('bouton-pin').onclick = function () {
      var pin = $('champ-pin').value;
      if (pin) { $('message-pin').textContent = 'Ouverture…'; ouvrir(pin); }
    };
    $('champ-pin').onkeydown = function (e) { if (e.keyCode === 13) { $('bouton-pin').onclick(); } };
    var pin = lirePin();
    if (pin) { ouvrir(pin); } else { montrerPin(''); }
  };

  window.addEventListener('load', S.demarrer);
}());
