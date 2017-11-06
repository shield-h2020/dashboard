export const MODAL_EVENT = {
  EMIT: {
    OPEN: 'emitModalOpen',
    CLOSE: 'emitModalClose',
  },
  CAST: {
    OPEN: 'castModalOpen',
    CLOSE: 'castModalClose',
  },
};

export const EDIT_MODAL_EVENT = {
  EMIT: {
    OPEN: 'emitEditModalOpen',
    CLOSE: 'emitEditModalClose',
  },
  CAST: {
    OPEN: 'castEditModalOpen',
    CLOSE: 'castEditModalClose',
  },
};

export const UPLOAD_MODAL_EVENT = {
  EMIT: {
    LOADING: 'emitLoadingUploadModal',
    OPEN: 'emitUploadModalOpen',
    CLOSE: 'emitUploadModalClose',
  },
  CAST: {
    LOADING: 'castLoadingUploadModal',
    OPEN: 'castUploadModalOpen',
    CLOSE: 'castUploadModalClose',
  },
};

export const TOGGLE_TOPOLOGY_EVENT = {
  CAST: 'castToggleTopology',
  EMIT: 'emitToggleTopology',
};

export const TOPOLOGY_DRAWER_EVENT = {
  CAST: 'castTopologyDrawer',
  EMIT: 'emitTopologyDrawer',
};

export const JSON_VIEWER_EVENT = {
  EMIT: {
    OPEN: 'emitJsonViewerOpen',
    CLOSE: 'emitJsonViewerClose',
  },
  CAST: {
    OPEN: 'castJsonViewerOpen',
    CLOSE: 'castJsonViewerClose',
  },
};
