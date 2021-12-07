if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    document.getElementById('replaceable').style.display='None';
}


function change() {
  let a = document.createElement('iframe')
  a.width = "560"
  a.height = "315"
  a.src = "https://www.youtube.com/embed/sAXZbfLzJUg?autoplay=1"
  let target = document.getElementById('replaceable')
  target.replaceWith(a)
};
