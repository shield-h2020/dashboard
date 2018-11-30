const webpack = require('webpack');
const webpackMerge = require('webpack-merge');
const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const commonConfig = require('./webpack.config.common');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

const DIR = process.cwd();

module.exports = webpackMerge(commonConfig, {
  output: {
    path: path.join(DIR, 'prod'),
    publicPath: '/',
    filename: '[name].[hash].js',
    chunkFilename: '[id].[hash].chunk.js',
  },

  plugins: [
    new ExtractTextPlugin('[name].[hash].css'),
    new CleanWebpackPlugin(['prod']),
    new webpack.DefinePlugin({
      /* A null value is given for the application to read from the window.location. */
      __API_URL__: null,
      __API_PORT__: JSON.stringify(process.env.BACKENDAPI_PORT),
      __API_STORE_HOST__: JSON.stringify(process.env.VNSF_STORE_HOST),
      __API_STORE_PORT__: JSON.stringify(process.env.VNSF_STORE_PORT),
      __API_SOCKET_PORT__: JSON.stringify(process.env.SKT_PORT),
      __INFLUXPORT__: JSON.stringify(process.env.INFLUXDB_PORT)
    }),
  ],
});
