const webpack = require('webpack');
const webpackMerge = require('webpack-merge');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const commonConfig = require('./webpack.config.common.js');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = webpackMerge(commonConfig, {
  output: {
    path: path.join(__dirname, 'prod'),
    publicPath: '/',
    filename: '[name].[hash].js',
    chunkFilename: '[id].[hash].chunk.js',
  },

  plugins: [
    new UglifyJSPlugin({
      compress: true,
      mangle: false,
    }),
    new ExtractTextPlugin('[name].[hash].css'),
    new CleanWebpackPlugin(['prod']),
    new webpack.DefinePlugin({
      /* A null value is given for the application to read from the window.location. */
      __API_URL__: null
    }),
  ],
});
