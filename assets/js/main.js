(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isRtl = () => root.dir === 'rtl';

  /* ---------------- copy (Arabic is the default, also present in the HTML) ---------------- */
  const I18N = {
    ar: {
      docTitle: 'Elegarden — تنسيق وتصميم الحدائق',
      metaDesc: 'تصميم الحدائق وتخطيطها وتنفيذها والعناية بها. ننشئ لك حديقة جميلة وعمليّة خلال 60 يوماً.',
      brandNote: '5 سنوات في خدمة جمال<br>الحدائق ووظيفتها',
      menu: 'القائمة',
      langBtn: 'EN',
      langAria: 'Switch to English',
      tagline: 'غيّر <em>تنسيق الحدائق</em> من حولك<br>وأبرِز شخصيتك المميّزة',
      lead: 'ننشئ لك حديقة جميلة<br>وعمليّة خلال',
      days: 'يوماً',
      scrollDown: 'انتقل للأسفل',
      navAbout: 'من نحن', navProjects: 'مشاريعنا', navServices: 'خدماتنا', navBlog: 'المدوّنة', navContacts: 'تواصل معنا',
      aboutTitle: 'نحرس <b>جمال</b><br><b>ووظيفة</b> حدائقكم',
      years: 'سنوات',
      ballAlt: 'كرة مشذّبة من نبات البقس',
      aboutLead: 'تقدّم Elegarden خدمات تنسيق الحدائق وتخطيطها وتنفيذها، وتجهيز المساحات الخارجية، والتشجير، والعناية بالحدائق وصيانتها.',
      aboutCopy: 'أُسِّست شركة Elegarden لتنسيق الحدائق لتحوّل فكرة حديقتك إلى واقع. نرسم فكرة الحديقة والتشجير مبكراً، قبل حلول دفء الربيع: نناقش التفاصيل، ونصوغ رغباتك، ونتابع معك كيف يتّخذ حلم حديقتك ملامحه الواضحة.',
      learnMore: 'اعرف المزيد',
      statsLabel: 'مشروعاً<span>منجزاً</span>',
      tabPrivate: 'حدائق خاصة', tabPublic: 'مساحات عامة',
      prev: 'السابق', next: 'التالي',
      servicesTitle: 'أبرز <span>خدماتنا</span>',
      details: 'التفاصيل',
      compassAlt: 'فرجار هندسي',
      niwakiAlt: 'شجرة نيواكي مشذّبة',
      svcPrev: 'الخدمة السابقة', svcNext: 'الخدمة التالية',
      blogTitle: 'من <span>مدوّنتنا</span>',
      contactsTitle: 'تواصل معنا',
      address: 'موسكو، شارع ناخيموفسكي<br>بروسبكت، مبنى 24',
      copyright: 'جميع الحقوق محفوظة. Elegarden 2020',
      read: 'اقرأ',
      area: 'مساحة التصميم:',
      quote: ['«', '»'],
    },
    en: {
      docTitle: 'Elegarden — Landscape design',
      metaDesc: 'Landscape design, planning, construction and garden care. We will create a beautiful and functional garden in 60 days.',
      brandNote: '5 years guarding the beauty<br>and functionality of gardens',
      menu: 'Menu',
      langBtn: 'عربي',
      langAria: 'التبديل إلى العربية',
      tagline: 'Change the <em>landscape design</em> around you<br>— express your individuality',
      lead: 'We will create a beautiful<br>and functional garden in',
      days: 'days',
      scrollDown: 'Scroll down',
      navAbout: 'About', navProjects: 'Projects', navServices: 'Services', navBlog: 'Blog', navContacts: 'Contacts',
      aboutTitle: 'guarding the <b>beauty</b><br><b>and functionality</b> of gardens',
      years: 'years',
      ballAlt: 'Clipped boxwood ball',
      aboutLead: 'Elegarden delivers landscape design, landscape planning, landscape construction, site improvement, greening, garden care and garden maintenance.',
      aboutCopy: 'The Elegarden landscape company was founded to turn the idea of your garden into reality. A garden and planting concept is shaped well in advance, before the spring warmth arrives — we discuss the details, refine your wishes and watch together as your dream garden takes clear shape.',
      learnMore: 'Learn more',
      statsLabel: 'Completed<span>projects</span>',
      tabPrivate: 'Private gardens', tabPublic: 'Public spaces',
      prev: 'Previous', next: 'Next',
      servicesTitle: 'Our <span>services</span>',
      details: 'Details',
      compassAlt: 'Drafting compass',
      niwakiAlt: 'Cloud-pruned niwaki tree',
      svcPrev: 'Previous service', svcNext: 'Next service',
      blogTitle: 'Our <span>blog</span>',
      contactsTitle: 'Contacts',
      address: 'Moscow, Nakhimovsky<br>Prospekt, bld. 24',
      copyright: 'All rights reserved. Elegarden 2020',
      read: 'Read',
      area: 'Design area:',
      quote: ['“', '”'],
    },
  };

  const PROJECT_IMGS = { private: ['project-1', 'project-2', 'project-3', 'project-6'], public: ['project-4', 'project-5', 'blog-3', 'blog-5'] };
  const CONTENT = {
    ar: {
      projects: {
        private: [
          ['حديقة خاصة في بلدة', 'روبليوفو', '4.5 هكتار', 'منطقة موسكو، 2018'],
          ['حديقة خاصة في بلدة', 'فاسيوكي-2', '4.5 هكتار', 'منطقة موسكو، 2018'],
          ['حديقة خاصة في بلدة', 'المدينة الذهبية', '4.5 هكتار', 'منطقة موسكو، 2018'],
          ['حديقة خاصة في بلدة', 'بارفيخا', '3.2 هكتار', 'منطقة موسكو، 2019'],
        ],
        public: [
          ['مساحة عامة', 'ساحة بريسنيا', '1.8 هكتار', 'موسكو، 2019'],
          ['مساحة عامة', 'ممشى النصر', '2.4 هكتار', 'موسكو، 2019'],
          ['مساحة عامة', 'حديقة البحيرة', '6.1 هكتار', 'ضواحي موسكو، 2020'],
          ['مساحة عامة', 'المتاهة', '0.9 هكتار', 'موسكو، 2020'],
        ],
      },
      blogTitle: 'أفضل 10 طرق: كيف تقلّل تكاليف إنشاء حديقة صغيرة والعناية بها؟',
      services: [['تخطيط', 'الحدائق'], ['الاستشارات', ''], ['التشجير', 'الداخلي'], ['تنفيذ', 'الحدائق'], ['تشجير', 'الأسطح']],
    },
    en: {
      projects: {
        private: [
          ['Private garden in', 'Rublevo', '4.5 ha', 'Moscow Region, 2018'],
          ['Private garden in', 'Vasyuki-2', '4.5 ha', 'Moscow Region, 2018'],
          ['Private garden in', 'Golden City', '4.5 ha', 'Moscow Region, 2018'],
          ['Private garden in', 'Barvikha', '3.2 ha', 'Moscow Region, 2019'],
        ],
        public: [
          ['Public space', 'Presnya Square', '1.8 ha', 'Moscow, 2019'],
          ['Public space', 'Victory Alley', '2.4 ha', 'Moscow, 2019'],
          ['Public space', 'Lakeside Park', '6.1 ha', 'Moscow suburbs, 2020'],
          ['Public space', 'The Labyrinth', '0.9 ha', 'Moscow, 2020'],
        ],
      },
      blogTitle: 'Top 10: how to optimise\nthe cost of creating\nand maintaining a small\ngarden?',
      services: [['Landscape', 'planning'], ['Consulting', ''], ['Interior', 'greening'], ['Landscape', 'construction'], ['Roof', 'greening']],
    },
  };
  const SERVICE_META = [
    { icon: 'i-bush', scene: 'ring-scene.jpg' },
    { icon: 'i-consult', scene: 'project-5.jpg' },
    { icon: 'i-flower', scene: 'blog-6.jpg' },
    { icon: 'i-bush', scene: 'project-1.jpg' },
    { icon: 'i-roof', scene: 'blog-4.jpg' },
  ];
  const BLOG_IMGS = ['blog-1', 'blog-2', 'blog-3', 'blog-4', 'blog-5', 'blog-6'];

  let lang = root.lang === 'en' ? 'en' : 'ar';
  const t = (key) => I18N[lang][key];
  const projectsFor = (tab) => CONTENT[lang].projects[tab].map(([kind, name, area, place], i) => ({ img: PROJECT_IMGS[tab][i], kind, name, area, place }));
  const blogItems = () => BLOG_IMGS.map((img) => ({ img, title: CONTENT[lang].blogTitle, date: '20/03/21' }));
  const services = () => CONTENT[lang].services.map(([a, b], i) => ({ a, b, ...SERVICE_META[i] }));

  /* ---------------- cards ---------------- */
  const eye = '<svg><use href="#i-eye"/></svg>';
  const quoted = (s) => `${t('quote')[0]}${s}${t('quote')[1]}`;
  const projectCard = (p, i) => `
    <article class="pcard">
      <div class="pcard__img"><img src="assets/img/${p.img}.jpg" alt="${p.kind} ${quoted(p.name)}" loading="lazy"></div>
      <div class="pcard__body">
        <p>${p.kind}</p>
        <b>${quoted(p.name)}</b>
        <span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
        <p>${t('area')} <strong>${p.area}</strong></p>
        <p>${p.place}</p>
      </div>
      <a class="pill" href="#contacts">${eye}<span>${t('details')}</span></a>
      <span class="pcard__num">${String(i + 1).padStart(2, '0')}</span>
    </article>`;
  const blogCard = (b) => `
    <article class="bcard">
      <div class="bcard__img"><img src="assets/img/${b.img}.jpg" alt="" loading="lazy"></div>
      <div class="bcard__body">
        <h3>${b.title}</h3>
        <span class="bcard__sep"></span>
        <time class="num">${b.date}</time>
      </div>
      <a class="pill" href="#blog">${eye}<span>${t('read')}</span></a>
    </article>`;

  /* ---------------- carousels (direction-aware) ---------------- */
  function carousel(board, render) {
    const track = $('.board__track', board);
    let index = 0;
    const step = () => {
      const card = track.firstElementChild;
      if (!card) return 0;
      return card.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0);
    };
    const visible = () => Math.max(1, Math.round(($('.board__viewport', board).clientWidth - 24 + 8) / step()));
    const apply = () => {
      const max = Math.max(0, track.children.length - visible());
      index = Math.min(Math.max(index, 0), max);
      // RTL tracks start at the right edge, so moving forward slides them right
      track.style.transform = `translateX(${(isRtl() ? 1 : -1) * index * step()}px)`;
      $$('.orb', board).forEach((b) => {
        const d = +b.dataset.dir;
        b.toggleAttribute('disabled', (d < 0 && index === 0) || (d > 0 && index === max));
        b.style.opacity = b.disabled ? '.45' : '';
      });
    };
    const set = (list) => { track.innerHTML = list.map(render).join(''); index = 0; apply(); };
    $$('.orb', board).forEach((b) => b.addEventListener('click', () => { index += +b.dataset.dir; apply(); }));
    addEventListener('resize', apply);
    let x0 = null;
    track.addEventListener('pointerdown', (e) => { x0 = e.clientX; });
    addEventListener('pointerup', (e) => {
      if (x0 === null) return;
      const dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) { index += (dx < 0) !== isRtl() ? 1 : -1; apply(); }
    });
    return { set, track };
  }

  const projectsBoard = $('#projects .board');
  const projects = carousel(projectsBoard, projectCard);
  const blog = carousel($('.board--blog'), blogCard);
  const activeTab = () => projectsBoard.dataset.active || 'private';

  $$('.board__tab', projectsBoard).forEach((tab) => tab.addEventListener('click', () => {
    if (tab.classList.contains('is-active')) return;
    $$('.board__tab', projectsBoard).forEach((el) => {
      const on = el === tab;
      el.classList.toggle('is-active', on);
      el.setAttribute('aria-selected', on);
    });
    projectsBoard.dataset.active = tab.dataset.tab;
    projects.track.classList.add('is-fading');
    setTimeout(() => {
      projects.set(projectsFor(tab.dataset.tab));
      requestAnimationFrame(() => projects.track.classList.remove('is-fading'));
    }, 300);
  }));

  /* ---------------- services wheel ---------------- */
  const svcTitle = $('.svc-title');
  const sceneImg = $('.ring__scene img');
  const tool = $('.ring__tool');
  const sides = { start: $('[data-side="start"]'), end: $('[data-side="end"]') };
  let current = 0;
  const at = (k) => { const list = services(); return list[(current + k + list.length * 4) % list.length]; };
  const titleHtml = (s) => `<b>${s.a}</b><span>${s.b || '&nbsp;'}</span>`;
  const item = (s, offset) => `
    <button class="svc-item" type="button" data-offset="${offset}">
      <svg><use href="#${s.icon}"/></svg><i></i><b>${s.a}</b><span>${s.b || '&nbsp;'}</span>
    </button>`;

  function renderSides(animate) {
    // previous two on the inline-start side, next two on the inline-end side (mirrors in RTL)
    sides.start.innerHTML = item(at(3), 3) + item(at(4), 4);
    sides.end.innerHTML = item(at(1), 1) + item(at(2), 2);
    if (animate) {
      $$('.svc-item').forEach((el, i) => {
        el.classList.add('is-entering');
        setTimeout(() => el.classList.remove('is-entering'), 60 + i * 60);
      });
    }
    $$('.svc-item').forEach((el) => el.addEventListener('click', () => go(+el.dataset.offset)));
  }

  function go(delta) {
    current = (current + delta + SERVICE_META.length) % SERVICE_META.length;
    const s = at(0);
    svcTitle.classList.add('is-swapping');
    sceneImg.classList.add('is-swapping');
    tool.style.transform = `rotate(${(delta > 0) !== isRtl() ? 14 : -14}deg)`;
    setTimeout(() => {
      svcTitle.innerHTML = titleHtml(s);
      sceneImg.src = `assets/img/${s.scene}`;
      svcTitle.classList.remove('is-swapping');
      sceneImg.classList.remove('is-swapping');
      tool.style.transform = '';
      renderSides(true);
    }, 320);
  }
  $('.ring__nav--prev').addEventListener('click', () => go(-1));
  $('.ring__nav--next').addEventListener('click', () => go(1));

  /* ---------------- language ---------------- */
  function applyLanguage() {
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.title = t('docTitle');
    $('meta[name="description"]').setAttribute('content', t('metaDesc'));
    $$('[data-i18n]').forEach((el) => { el.innerHTML = t(el.dataset.i18n); });
    $$('[data-i18n-aria]').forEach((el) => el.setAttribute('aria-label', t(el.dataset.i18nAria)));
    $$('[data-i18n-alt]').forEach((el) => { el.alt = t(el.dataset.i18nAlt); });
    projects.set(projectsFor(activeTab()));
    blog.set(blogItems());
    svcTitle.innerHTML = titleHtml(at(0));
    renderSides(false);
  }

  $('.lang').addEventListener('click', () => {
    lang = lang === 'ar' ? 'en' : 'ar';
    try { localStorage.setItem('eg-lang', lang); } catch (e) { /* storage blocked: choice lasts for this view only */ }
    const url = new URL(location.href);
    if (url.searchParams.has('lang')) { url.searchParams.set('lang', lang); history.replaceState(null, '', url); }
    applyLanguage();
  });
  applyLanguage();

  /* ---------------- menu ---------------- */
  const burger = $('.burger');
  const menu = $('#menu');
  const toggleMenu = (open) => {
    burger.setAttribute('aria-expanded', open);
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', !open);
    document.body.classList.toggle('menu-open', open);
  };
  burger.addEventListener('click', () => toggleMenu(burger.getAttribute('aria-expanded') !== 'true'));
  $$('a', menu).forEach((a) => a.addEventListener('click', () => toggleMenu(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape') toggleMenu(false); });

  /* ---------------- reveal on scroll ---------------- */
  const io = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  $$('[data-reveal]').forEach((el, i) => {
    el.style.transitionDelay = `${(i % 4) * 70}ms`;
    io.observe(el);
  });

  if (reduced) return;

  /* ---------------- depth / parallax ---------------- */
  const depthEls = $$('[data-depth]');
  const ball = $('.about__ball');
  let mx = 0, my = 0, raf = 0;
  addEventListener('pointermove', (e) => {
    mx = e.clientX / innerWidth - 0.5;
    my = e.clientY / innerHeight - 0.5;
    if (!raf) raf = requestAnimationFrame(frame);
  });
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(frame); }, { passive: true });
  function frame() {
    raf = 0;
    const sy = scrollY;
    // `translate` / `rotate` compose with each element's own CSS transform
    depthEls.forEach((el) => {
      const d = +el.dataset.depth;
      el.style.translate = `${(-mx * d).toFixed(1)}px ${(-my * d + sy * d * 0.004).toFixed(1)}px`;
    });
    ball.style.rotate = `${(sy * 0.04).toFixed(2)}deg`;
  }
})();
