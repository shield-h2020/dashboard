import angular from 'angular';

const SIZE_FOOTER = 90;
const MARGIN_BOTTOM = 38;

export const AutoResizerDirective = ($window) => {
  'ngInject';

  return {
    restrict: 'A',
    link(scope, element) {
      const onResize = () => {
        const wHeight = $window.innerHeight;
        const parent = element.parent();
        // remove magic number for total margins
        const titleHeight = parent.children(0).prop('offsetHeight');
        const availableHeight = wHeight - titleHeight - MARGIN_BOTTOM - SIZE_FOOTER;
        element.css('height', `${availableHeight}px`);
      };

      onResize();
      angular.element($window).on('resize', onResize);

      scope.$on('$destroy', () => {
        angular.element($window).off('resize', onResize);
      });
    },
  };
};

export default AutoResizerDirective;
