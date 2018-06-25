import angular from 'angular';

export const CollapsibleDirective = () => ({
  restrict: 'A',
  link(scope, element) {
    const found = element.find('h5');
    const content = angular.element(element.children()[1]);

    if (content) {
      setTimeout(() => {
        content.addClass('collapsed');
        element.addClass('isCollapsed');
      }, 0);
    }

    if (found) {
      found.append('<span class="collapse_icon"></span>');
    }

    element.on('click', () => {
      if (content.hasClass('collapsed')) {
        content.removeClass('collapsed');
        element.removeClass('isCollapsed');
      } else {
        content.addClass('collapsed');
        element.addClass('isCollapsed');
      }
    });
  },
});

export default CollapsibleDirective;
