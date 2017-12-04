export const InputFocusDirective = $timeout => ({

  restrict: 'A',
  scope: {
    trigger: '<focus',
  },
  link(scope, element) {
    scope.$watch('trigger', (value) => {
      if (value) {
        $timeout(() => {
          element[0].focus();
        });
      }
    });
  },
});

export default InputFocusDirective;
