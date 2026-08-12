(function(){
'use strict';
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* progress bar */
var pbar=document.querySelector('.progress-bar');
if(pbar){window.addEventListener('scroll',function(){var h=document.documentElement,pct=(h.scrollTop/(h.scrollHeight-h.clientHeight))*100;pbar.style.width=Math.min(100,Math.max(0,pct))+'%'},{passive:true})}

/* floating CTA */
var fcta=document.querySelector('.float-cta');
if(fcta){var last=0,heroH=0,hero=document.querySelector('.hero,section.block:first-of-type');if(hero)heroH=hero.offsetHeight;window.addEventListener('scroll',function(){var y=window.scrollY;if(y>heroH*.8&&y>last)fcta.classList.add('visible');else if(y<heroH*.4)fcta.classList.remove('visible');last=y},{passive:true})}

/* back-to-top */
var btt=document.querySelector('.back-to-top');
if(btt){window.addEventListener('scroll',function(){btt.classList.toggle('visible',window.scrollY>400)},{passive:true});btt.addEventListener('click',function(){window.scrollTo({top:0,behavior:reduce?'auto':'smooth'})})}

/* hamburger — single binder (guard against duplicate listeners) */
var t=document.getElementById('menuToggle'),m=document.getElementById('mobileNav');
if(t&&m&&!t.dataset.menuBound){
  t.dataset.menuBound='1';
  function setOpen(o){
    m.classList.toggle('open',o);
    t.setAttribute('aria-expanded',o?'true':'false');
    t.setAttribute('aria-label',o?'Stäng meny':'Öppna meny');
  }
  t.addEventListener('click',function(){setOpen(!m.classList.contains('open'));});
  m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setOpen(false);});});
}
})();
