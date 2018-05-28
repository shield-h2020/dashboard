export const ActionFeedbackDirective = ($timeout, $compile, $interpolate) => ({

  restrict: 'A',
  scope: {
    trigger: '<actionFeedback',
  },
  link(scope, element, attrs) {
    const prevText = element.text().slice(0);
    const action = attrs.action;
    const appendix = $compile('<i class="animate--rotating-light"></i>')(scope);

    scope.$watch('trigger', (value, oldValue) => {
      if (value !== oldValue) {
        if (value) {
          $timeout(() => {
            element.prop('disabled', true);
            if (action) {
              element.text(`...${action}`);
            }
            element.prepend(appendix);
          });
        } else {
          $timeout(() => {
            element.prop('disabled', false);
            element.text($interpolate(prevText)(scope.$parent));
            $compile(element)(scope);
          });
        }
      }
    });
  },
});

export default ActionFeedbackDirective;
