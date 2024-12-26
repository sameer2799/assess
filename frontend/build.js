const esbuild = require('esbuild');
const { sassPlugin } = require('esbuild-sass-plugin');
const postCssPlugin = require('esbuild-style-plugin');
const server = require('live-server');
const production = process.env.NODE_ENV === 'production';

esbuild.build({
  entryPoints: ['src/index.jsx'],
  bundle: true,
  minify: production,
  sourcemap: !production,
  outdir: '.',
  loader: {
    '.js': 'jsx',
    '.svg': 'dataurl',
    '.png': 'dataurl',
    '.jpg': 'dataurl',
    '.gif': 'dataurl',
  },
  plugins: [
    sassPlugin(),
    postCssPlugin({
      postcss: {
        plugins: [require('autoprefixer')],
      },
    }),
  ],
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
  },
  target: ['chrome58', 'firefox57', 'safari11', 'edge18'], 
}).then(() => {
  if (!production) {
    server.start({
      root: '.',
      open: 'index.html',
      wait: 500,
      cors: true,
  })}
}).catch(() => process.exit(1));
