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

/* hamburger */
var t=document.getElementById('menuToggle'),m=document.getElementById('mobileNav');
if(t&&m){t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');var ic=t.querySelector('.hamburger-icon'),cl=t.querySelector('.hamburger-close');if(ic)ic.style.display=o?'none':'';if(cl)cl.style.display=o?'':''});m.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){m.classList.remove('open');t.setAttribute('aria-expanded','false');var ic=t.querySelector('.hamburger-icon'),cl=t.querySelector('.hamburger-close');if(ic)ic.style.display='';if(cl)cl.style.display='none'})})}
})();
