'use strict';
const form = document.querySelector('.filters');
const search = document.getElementById('search');
const degree = document.getElementById('degree');
const year = document.getElementById('year');
const cards = [...document.querySelectorAll('.project')];
const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
function filter() {
  if (degree.value === 'UNIR') year.value = '';
  year.disabled = degree.value === 'UNIR';
  const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  for (const card of cards) {
    const visible = (!degree.value || card.dataset.degree === degree.value)
      && (!year.value || card.dataset.year === year.value)
      && words.every(word => normalize(card.dataset.search).includes(word));
    card.hidden = !visible;
    if (visible) count++;
  }
  for (const subject of document.querySelectorAll('.subject')) {
    subject.hidden = ![...subject.querySelectorAll('.project')].some(card => !card.hidden);
  }
  for (const course of document.querySelectorAll('.course')) {
    course.hidden = ![...course.querySelectorAll('.subject')].some(subject => !subject.hidden);
  }
  document.getElementById('result-count').textContent = `${count} ${count === 1 ? 'entrada' : 'entradas'}`;
  document.getElementById('empty').hidden = count !== 0;
}
form.hidden = false;
form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('input', filter);
form.addEventListener('change', filter);
form.addEventListener('reset', () => { setTimeout(filter, 0); });
for (const link of document.querySelectorAll('.side nav a')) {
  link.addEventListener('click', () => { form.reset(); filter(); });
}
filter();
