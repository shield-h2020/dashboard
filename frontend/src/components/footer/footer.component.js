import template from './footer.html';
import styles from './footer.scss';

const UI_STRINGS = {
  text: 'This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 700199',
};

export const FooterComponent = {
  template,
  controller: class FooterComponent {
    constructor() {
      this.strings = UI_STRINGS;
      this.styles = styles;
    }
  },
};

export default FooterComponent;
