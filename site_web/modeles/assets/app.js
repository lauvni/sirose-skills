// Contrôle d'âge (vente d'alcool) et menu mobile. Aucun cookie : la réponse
// au contrôle d'âge est gardée en sessionStorage, effacée à la fermeture de l'onglet.
(function () {
  var porte = document.getElementById('controle-age');
  if (porte) {
    var dejaValide = false;
    try { dejaValide = sessionStorage.getItem('sirose-majeur') === 'oui'; } catch (e) {}
    if (!dejaValide) {
      porte.hidden = false;
      document.body.classList.add('bloque');
      porte.querySelector('[data-age="oui"]').focus();
    }
    porte.querySelector('[data-age="oui"]').addEventListener('click', function () {
      try { sessionStorage.setItem('sirose-majeur', 'oui'); } catch (e) {}
      porte.hidden = true;
      document.body.classList.remove('bloque');
    });
  }

  var bouton = document.querySelector('.menu-bouton');
  var menu = document.getElementById('menu');
  if (bouton && menu) {
    bouton.addEventListener('click', function () {
      var ouvert = bouton.getAttribute('aria-expanded') === 'true';
      bouton.setAttribute('aria-expanded', String(!ouvert));
      menu.classList.toggle('ouvert', !ouvert);
    });
  }
})();
