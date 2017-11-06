const webpack = require('webpack');
const webpackMerge = require('webpack-merge');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const commonConfig = require('./webpack.config.common.js');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = webpackMerge(commonConfig, {
  output: {
    path: path.join(__dirname, 'dev'),
    publicPath: '/',
    filename: '[name].bundle.js',
    chunkFilename: '[id].chunk.js',
  },
  watch: false,
  plugins: [
    new ExtractTextPlugin('[name].css'),
    new CleanWebpackPlugin(['dev']),
    new webpack.DefinePlugin({
      __API_URL__: "'localhost'"
    }),
  ],
});
