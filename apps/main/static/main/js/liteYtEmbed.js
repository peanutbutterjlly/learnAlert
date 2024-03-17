export class LiteYTEmbed extends HTMLElement {
  constructor() {
    super(), (this.isIframeLoaded = !1), this.setupDom();
  }
  static get observedAttributes() {
    return ['videoid', 'playlistid'];
  }
  connectedCallback() {
    this.addEventListener('pointerover', LiteYTEmbed.warmConnections, {
      once: !0,
    }),
      this.addEventListener('click', () => this.addIframe());
  }
  get videoId() {
    return encodeURIComponent(this.getAttribute('videoid') || '');
  }
  set videoId(e) {
    this.setAttribute('videoid', e);
  }
  get playlistId() {
    return encodeURIComponent(this.getAttribute('playlistid') || '');
  }
  set playlistId(e) {
    this.setAttribute('playlistid', e);
  }
  get videoTitle() {
    return this.getAttribute('videotitle') || 'Video';
  }
  set videoTitle(e) {
    this.setAttribute('videotitle', e);
  }
  get videoPlay() {
    return this.getAttribute('videoPlay') || 'Play';
  }
  set videoPlay(e) {
    this.setAttribute('videoPlay', e);
  }
  get videoStartAt() {
    return this.getAttribute('videoStartAt') || '0';
  }
  get autoLoad() {
    return this.hasAttribute('autoload');
  }
  get noCookie() {
    return this.hasAttribute('nocookie');
  }
  get posterQuality() {
    return this.getAttribute('posterquality') || 'hqdefault';
  }
  get posterLoading() {
    return this.getAttribute('posterloading') || 'lazy';
  }
  get params() {
    return `start=${this.videoStartAt}&${this.getAttribute('params')}`;
  }
  set params(e) {
    this.setAttribute('params', e);
  }
  setupDom() {
    const e = this.attachShadow({ mode: 'open' });
    let t = '';
    window.liteYouTubeNonce && (t = `nonce="${window.liteYouTubeNonce}"`),
      (e.innerHTML = `\n      <style ${t}>\n        :host {\n          contain: content;\n          display: block;\n          position: relative;\n          width: 100%;\n          padding-bottom: calc(100% / (16 / 9));\n        }\n\n        @media (max-width: 40em) {\n          :host([short]) {\n            padding-bottom: calc(100% / (9 / 16));\n          }\n        }\n\n        #frame, #fallbackPlaceholder, iframe {\n          position: absolute;\n          width: 100%;\n          height: 100%;\n          left: 0;\n        }\n\n        #frame {\n          cursor: pointer;\n        }\n\n        #fallbackPlaceholder {\n          object-fit: cover;\n        }\n\n        #frame::before {\n          content: '';\n          display: block;\n          position: absolute;\n          top: 0;\n          background-image: linear-gradient(180deg, #111 -20%, transparent 90%);\n          height: 60px;\n          width: 100%;\n          z-index: 1;\n        }\n\n        #playButton {\n          width: 68px;\n          height: 48px;\n          background-color: transparent;\n          background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 68 48"><path d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79.13 34 0 34 0S12.21.13 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C.06 13.05 0 24 0 24s.06 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 47.87 34 48 34 48s21.79-.13 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C67.94 34.95 68 24 68 24s-.06-10.95-1.48-16.26z" fill="red"/><path d="M45 24 27 14v20" fill="white"/></svg>');\n          z-index: 1;\n          border: 0;\n          border-radius: inherit;\n        }\n\n        #playButton:before {\n          content: '';\n          border-style: solid;\n          border-width: 11px 0 11px 19px;\n          border-color: transparent transparent transparent #fff;\n        }\n\n        #playButton,\n        #playButton:before {\n          position: absolute;\n          top: 50%;\n          left: 50%;\n          transform: translate3d(-50%, -50%, 0);\n          cursor: inherit;\n        }\n\n        /* Post-click styles */\n        .activated {\n          cursor: unset;\n        }\n\n        #frame.activated::before,\n        #frame.activated > #playButton {\n          display: none;\n        }\n      </style>\n      <div id="frame">\n        <picture>\n          <source id="webpPlaceholder" type="image/webp">\n          <source id="jpegPlaceholder" type="image/jpeg">\n          <img id="fallbackPlaceholder" referrerpolicy="origin" loading="lazy">\n        </picture>\n        <button id="playButton"></button>\n      </div>\n    `),
      (this.domRefFrame = e.querySelector('#frame')),
      (this.domRefImg = {
        fallback: e.querySelector('#fallbackPlaceholder'),
        webp: e.querySelector('#webpPlaceholder'),
        jpeg: e.querySelector('#jpegPlaceholder'),
      }),
      (this.domRefPlayButton = e.querySelector('#playButton'));
  }
  setupComponent() {
    this.initImagePlaceholder(),
      this.domRefPlayButton.setAttribute(
        'aria-label',
        `${this.videoPlay}: ${this.videoTitle}`
      ),
      this.setAttribute('title', `${this.videoPlay}: ${this.videoTitle}`),
      (this.autoLoad || this.isYouTubeShort()) &&
        this.initIntersectionObserver();
  }
  attributeChangedCallback(e, t, i) {
    switch (e) {
      case 'videoid':
      case 'playlistid':
      case 'videoTitle':
      case 'videoPlay':
        t !== i &&
          (this.setupComponent(),
          this.domRefFrame.classList.contains('activated') &&
            (this.domRefFrame.classList.remove('activated'),
            this.shadowRoot.querySelector('iframe').remove(),
            (this.isIframeLoaded = !1)));
        break;
      default:
        break;
    }
  }
  addIframe(e = !1) {
    if (!this.isIframeLoaded) {
      let t = e ? 0 : 1;
      const i = this.noCookie ? '-nocookie' : '';
      let o;
      (o = this.playlistId
        ? `?listType=playlist&list=${this.playlistId}&`
        : `${this.videoId}?`),
        this.isYouTubeShort() &&
          ((this.params = `loop=1&mute=1&modestbranding=1&playsinline=1&rel=0&enablejsapi=1&playlist=${this.videoId}`),
          (t = 1));
      const n = `\n<iframe frameborder="0" title="${this.videoTitle}"\n  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen\n  src="https://www.youtube${i}.com/embed/${o}autoplay=${t}&${this.params}"\n></iframe>`;
      this.domRefFrame.insertAdjacentHTML('beforeend', n),
        this.domRefFrame.classList.add('activated'),
        (this.isIframeLoaded = !0),
        this.attemptShortAutoPlay(),
        this.dispatchEvent(
          new CustomEvent('liteYoutubeIframeLoaded', {
            detail: { videoId: this.videoId },
            bubbles: !0,
            cancelable: !0,
          })
        );
    }
  }
  initImagePlaceholder() {
    const e = `https://i.ytimg.com/vi_webp/${this.videoId}/${this.posterQuality}.webp`,
      t = `https://i.ytimg.com/vi/${this.videoId}/${this.posterQuality}.jpg`;
    (this.domRefImg.fallback.loading = this.posterLoading),
      (this.domRefImg.webp.srcset = e),
      (this.domRefImg.jpeg.srcset = t),
      (this.domRefImg.fallback.src = t),
      this.domRefImg.fallback.setAttribute(
        'aria-label',
        `${this.videoPlay}: ${this.videoTitle}`
      ),
      this.domRefImg?.fallback?.setAttribute(
        'alt',
        `${this.videoPlay}: ${this.videoTitle}`
      );
  }
  initIntersectionObserver() {
    new IntersectionObserver(
      (e, t) => {
        e.forEach((e) => {
          e.isIntersecting &&
            !this.isIframeLoaded &&
            (LiteYTEmbed.warmConnections(),
            this.addIframe(!0),
            t.unobserve(this));
        });
      },
      { root: null, rootMargin: '0px', threshold: 0 }
    ).observe(this);
  }
  attemptShortAutoPlay() {
    this.isYouTubeShort() &&
      setTimeout(() => {
        this.shadowRoot
          .querySelector('iframe')
          ?.contentWindow?.postMessage(
            '{"event":"command","func":"playVideo","args":""}',
            '*'
          );
      }, 2e3);
  }
  isYouTubeShort() {
    return (
      '' === this.getAttribute('short') &&
      window.matchMedia('(max-width: 40em)').matches
    );
  }
  static addPrefetch(e, t) {
    const i = document.createElement('link');
    (i.rel = e),
      (i.href = t),
      (i.crossOrigin = 'true'),
      document.head.append(i);
  }
  static warmConnections() {
    LiteYTEmbed.isPreconnected ||
      window.liteYouTubeIsPreconnected ||
      (LiteYTEmbed.addPrefetch('preconnect', 'https://i.ytimg.com/'),
      LiteYTEmbed.addPrefetch('preconnect', 'https://s.ytimg.com'),
      LiteYTEmbed.addPrefetch('preconnect', 'https://www.youtube.com'),
      LiteYTEmbed.addPrefetch('preconnect', 'https://www.google.com'),
      LiteYTEmbed.addPrefetch(
        'preconnect',
        'https://googleads.g.doubleclick.net'
      ),
      LiteYTEmbed.addPrefetch('preconnect', 'https://static.doubleclick.net'),
      (LiteYTEmbed.isPreconnected = !0),
      (window.liteYouTubeIsPreconnected = !0));
  }
}
(LiteYTEmbed.isPreconnected = !1),
  customElements.define('lite-youtube', LiteYTEmbed);
