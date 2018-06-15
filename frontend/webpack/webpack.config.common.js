const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const DIR = process.cwd();

module.exports = {
  entry: {
    vendor: ['angular', '@uirouter/angularjs', 'd3', 'date-fns'],
    app: './src/app.module.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              'es2015',
              ['es2015', { modules: false }],
            ],
            plugins: ['transform-es2015-destructuring', 'transform-object-rest-spread'],
          },
        },
      },
      {
        test: /^((?!\.global).)*\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            { loader: 'css-loader?modules' },
            { loader: 'sass-loader' },
          ],
        }),
      },
      {
        test: /\.global\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            { loader: 'css-loader' },
            { loader: 'sass-loader' },
          ],
        }),
      },
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            { loader: 'css-loader' },
          ],
        }),
      },
      {
        test: /\.html$/,
        use: {
          loader: 'html-loader',
        },
      },
      {
        test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
        include: [
          path.resolve(DIR, 'node_modules', 'bootstrap-sass', 'assets', 'fonts'),
          path.resolve(DIR, 'src', 'assets', 'fonts')],
        use: {
          loader: 'file-loader?name=fonts/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: path.resolve(DIR, 'src', 'assets', 'images', 'network'),
        use: {
          loader: 'file-loader?name=images/network/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: [
          path.resolve(DIR, 'src', 'assets', 'images'),
          path.resolve(DIR, 'src', 'components'),
        ],
        exclude: [
          path.resolve(DIR, 'src', 'assets', 'images', 'icons'),
          path.resolve(DIR, 'src', 'assets', 'images', 'network'),
        ],
        use: {
          loader: 'file-loader?name=images/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: path.resolve(DIR, 'src', 'assets', 'images', 'icons'),
        use: {
          loader: 'file-loader?name=images/icons/[name].[ext]',
        },
      },
      {
        test: /\.png?$/,
        use: {
          loader: 'file-loader?name=images/[name].[ext]',
        },
      },
    ],
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      minChunks: Infinity,
    }),
    new HtmlWebpackPlugin({ template: 'index.html' }),
  ],
  resolve: {
    alias: {
      styleglobals: path.join(DIR, 'src', 'styles', 'globals'),
      api: path.join(DIR, 'src', 'api'),
      assets: path.join(DIR, 'src', 'assets'),
      components: path.join(DIR, 'src', 'components'),
    },
  },
  node: {
    fs: 'empty',
    tls: 'empty',
    ws: 'empty',
  },
  stats: {
    warnings: false,
  },
};
