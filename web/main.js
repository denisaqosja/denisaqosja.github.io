'use strict';
const menuToggle = document.querySelector('.nav-toggle');
const mainNavigation = document.querySelector('#main-navigation');
if (menuToggle && mainNavigation) {
  const setMenuOpen = open => {
    mainNavigation.dataset.open = String(open);
    menuToggle.setAttribute('aria-expanded', String(open));
  };
  menuToggle.addEventListener('click', () => {
    setMenuOpen(menuToggle.getAttribute('aria-expanded') !== 'true');
  });
  mainNavigation.addEventListener('click', event => {
    if (event.target.closest('a')) setMenuOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
      setMenuOpen(false);
      menuToggle.focus();
    }
  });
  setMenuOpen(false);
  document.querySelector('.site-header').classList.add('menu-ready');
}
const search = document.querySelector('#paper-search');
if (search) {
  search.addEventListener('input', () => {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    document.querySelectorAll('.publication').forEach(paper => {
      paper.hidden = !terms.every(term => paper.dataset.search.includes(term));
      if (!paper.hidden) count++;
    });
    document.querySelector('#result-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('#no-results').hidden = count !== 0;
  });
}
document.querySelectorAll('.copy-citation').forEach(button => {
  button.addEventListener('click', async () => {
    const text = document.getElementById(button.dataset.copy).textContent;
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = 'Copied';
      document.querySelector('#announcement').textContent = 'Citation copied to clipboard.';
      window.setTimeout(() => { button.textContent = 'Copy citation'; }, 2000);
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(document.getElementById(button.dataset.copy));
      selection.removeAllRanges(); selection.addRange(range);
      button.textContent = 'Selected — use Ctrl/Cmd+C';
      document.querySelector('#announcement').textContent = 'Citation selected. Use your keyboard to copy it.';
    }
  });
});
const velocity = document.querySelector('#velocity');
if (velocity) {
  const grid = document.querySelector('#demo-grid');
  const ns = 'http://www.w3.org/2000/svg';
  const make = (tag, attrs, text) => {
    const element = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key,value]) => element.setAttribute(key, value));
    if (text !== undefined) element.textContent = text;
    grid.append(element);
  };
  [0,.5,1].forEach(amplitude => {
    const y = 190 - amplitude * 160;
    make('line', {x1:52,y1:y,x2:735,y2:y,stroke:'#dce3e9'});
    make('text', {x:40,y:y+4,'text-anchor':'end'}, amplitude.toFixed(1));
  });
  [-10,-5,0,5,10].forEach(value => {
    const x = 52+(value+10)/20*683;
    make('line',{x1:x,y1:25,x2:x,y2:190,stroke:'#e7edf1'});
    make('text',{x,y:212,'text-anchor':'middle'},String(value));
  });
  make('text',{x:52,y:16},'Normalized power');
  const update = () => {
    const speed = Number(velocity.value);
    document.querySelector('#velocity-value').textContent = `${speed.toFixed(1)} m/s`;
    const points = Array.from({length:701},(_,i) => {
      const v = -10 + i/700*20;
      const z = Math.PI*(v-speed)/.65;
      const power = Math.abs(z) < 1e-10 ? 1 : (Math.sin(z)/z)**2;
      return `${i?'L':'M'}${(52+i/700*683).toFixed(2)},${(190-power*160).toFixed(2)}`;
    });
    document.querySelector('#demo-path').setAttribute('d',points.join(' '));
    document.querySelector('#demo-desc').textContent = `Normalized sinc-squared Doppler response, with its peak at ${speed.toFixed(1)} metres per second.`;
  };
  velocity.addEventListener('input',update); update();
}
