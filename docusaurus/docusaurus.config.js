// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Der Spiegel Translator',
  tagline: 'Learn German through Der Spiegel Bluesky posts',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-site.example.com',
  baseUrl: '/',

  organizationName: 'your-org',
  projectName: 'das-spiegel-translator',

  onBrokenLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.jpg',
      colorMode: {
        defaultMode: 'light',
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Der Spiegel Translator',
        logo: {
          alt: 'Der Spiegel Translator Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Posts',
          },
          {
            href: 'https://bsky.app/profile/derspiegel.bsky.social',
            label: 'Der Spiegel on Bluesky',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              {
                label: 'All Posts',
                to: '/',
              },
            ],
          },
          {
            title: 'Sources',
            items: [
              {
                label: 'Der Spiegel',
                href: 'https://www.spiegel.de',
              },
              {
                label: 'Bluesky',
                href: 'https://bsky.app/profile/derspiegel.bsky.social',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'German Dictionary',
                href: 'https://www.dict.cc',
              },
              {
                label: 'Docusaurus',
                href: 'https://docusaurus.io',
              },
            ],
          },
        ],
        copyright: `German learning resource. Posts from Der Spiegel. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
