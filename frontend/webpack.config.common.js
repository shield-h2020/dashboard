const webpack = require('webpack');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  entry: {
    vendor: ['angular', '@uirouter/angularjs', 'd3', 'date-fns'],
    app: './app/app.module.js',
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
          path.resolve(__dirname, 'node_modules', 'bootstrap-sass', 'assets', 'fonts'),
          path.resolve(__dirname, 'app', 'resources', 'fonts')],
        use: {
          loader: 'file-loader?name=fonts/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: path.resolve(__dirname, 'app', 'resources', 'images', 'network'),
        use: {
          loader: 'file-loader?name=images/network/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: [
          path.resolve(__dirname, 'app', 'resources', 'images'),
          path.resolve(__dirname, 'app', 'components', 'table', 'assets'),
        ],
        exclude: [
          path.resolve(__dirname, 'app', 'resources', 'images', 'icons'),
          path.resolve(__dirname, 'app', 'resources', 'images', 'network'),
        ],
        use: {
          loader: 'file-loader?name=images/[name].[ext]',
        },
      },
      {
        test: /\.svg(\?[a-z0-9=&.]+)?$/,
        include: path.resolve(__dirname, 'app', 'resources', 'images', 'icons'),
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
      styleglobals: path.join(__dirname, 'app', 'styles', 'globals'),
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
