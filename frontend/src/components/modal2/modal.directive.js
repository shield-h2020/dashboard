import styles from './modal.scss';

const TEMPLATE = `<div class="{{::styles.modal}} {{::styles['modal--hidden']}}">
<div class="{{::styles.background}}"></div>
<div class="{{::styles.container}} {{::styles.modal}}">
    <header class="{{::styles.header}}">{{title}}</header>
    <div class="{{::styles.content}}" ng-transclude="content"></div>
    <div class="{{::styles.footer}}" ng-transclude="buttons"></div>
</div>
</div>`;

export const ModalDirective = () => {
  'ngInject';

  return {
    restrict: 'A',
    transclude: {
      content: 'article',
      buttons: 'footer',
    },
    scope: {
      title: '<',
      open: '<',
    },
    replace: true,
    template: TEMPLATE,
    link(scope, element) {
      scope.styles = styles;
      scope.$watch('open', (newVal) => {
        console.log(newVal)
        if (newVal) {
          element.removeClass(scope.styles['modal--hidden']);
        } else {
          element.addClass(scope.styles['modal--hidden']);
        }
      });
    },
  };
};

export default ModalDirective;
