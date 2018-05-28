import styles from './table.scss';

export const ColorCellDirective = ($compile, $timeout) => ({
  restrict: 'A',
  link(scope, element) {
    $timeout(() => {
      const cellText = element.text().slice(0);
      if (cellText !== 'ok') {
        if (cellText === 'warn') {
          element.addClass(styles.warn);
        }

        if (cellText === 'error') {
          element.addClass(styles.error);
        }
      }
    }, 1000);
  },
});

export default ColorCellDirective;
