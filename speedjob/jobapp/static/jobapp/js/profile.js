let toggle = false;

window.onload = function() {
  document.getElementById('collapseThis').style.display = 'None';
};

function toggleForm() {
  toggle = !toggle;

  if (toggle)
    document.getElementById('collapseThis').style.display = 'inline-block';
  else
    document.getElementById('collapseThis').style.display = 'None';

}
