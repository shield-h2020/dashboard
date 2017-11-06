export const AutoResizerDirective = ($window) => {
  'ngInject';

  return {
    restrict: 'A',
    link(scope, element) {
      const wHeight = $window.innerHeight;
      const parent = element.parent();
// remove magic number for total margins
      const titleHeight = parent.children(0).prop('offsetHeight');
      const availableHeight = wHeight - titleHeight - 48;
      element.css('height', `${availableHeight}px`);
    },
  };
};

export default AutoResizerDirective;
