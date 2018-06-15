/*
* The HOST URL is picked up according to the environment defined at build time.
* If a development build is made the HOST is given by variable replacement.
* Else the HOST is read from the window's location.
*/

/* global
  window
  __API_URL__
  __API_PORT__
  __API_STORE_HOST__
  __API_STORE_PORT__
  __API_SOCKET_PORT__
*/
const BACKEND_HOST = window.location.hostname;
const API_PORT = 13030 || __API_PORT__;
const SOCKET_PORT = __API_SOCKET_PORT__;
const STORE_PORT = __API_STORE_PORT__;

const API_URL = `http://${'localhost' || __API_URL__ || BACKEND_HOST}`;
const SOCKET_URL = `ws://${BACKEND_HOST}`;
const STORE_URL = `http://${__API_STORE_HOST__}`;

export const AUTH_ADDRESS = `${API_URL}:${API_PORT}`;
export const API_ADDRESS = `${API_URL}:${API_PORT}`;
export const CATALOG_ADDRESS = `${API_URL}:${API_PORT}`;
export const SOCKET_ADDRESS = `${SOCKET_URL}:${SOCKET_PORT}`;
export const STORE_ADDRESS = `${STORE_URL}:${STORE_PORT}`;

export const ACC_ID = '{#id}';
export const ACC_NID = '{##id}';
