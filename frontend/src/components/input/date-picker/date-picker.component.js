import format from 'date-fns/format';
import template from './date-picker.html';
import styles from './date-picker.scss';

export const DatePickerComponent = {
  template,
  bindings: {
    label: '@?',
    onChange: '&',
    dateFormat: '<?',
    year: '<?',
    month: '<?',
    day: '<?',
    hour: '<?',
    minute: '<?',
    dateOnly: '<?',
    futureOnly: '<?',
    startDate: '<?',
    endDate: '<?',
    closeOnSelect: '<?',
    currentDate: '<?',
  },
  controller: class DatePickerComponent {
    constructor($locale) {
      'ngInject';

      this.locale = $locale;
      this.styles = styles;
      this.openPicker = false;
      this.calendar = this.buildCalendar();
    }

    $onInit() {
      console.log(this.currentDate)
      if (this.currentDate) {
        this.selectedDate = new Date(this.currentDate);
        this.showDate = format(this.selectedDate, this.dateFormat || 'YYYY-MM-DD HH:mm');
      }

      const today = new Date();
      if (!this.selectedDate || isNaN(this.selectedDate.getTime())) { // no predefined date
        const year = this.year || today.getFullYear();
        const month = this.month ? (this.month - 1) : today.getMonth();
        const day = this.day || today.getDate();
        const hour = this.hour || this.hour === 0 ? this.hour : today.getHours();
        const minute = this.minute || this.minute === 0 ? this.minute : today.getMinutes();
        this.selectedDate = new Date(year, month, day, hour, minute, 0);
        this.showDate = format(this.selectedDate, this.dateFormat || 'YYYY-MM-DD HH:mm');
      }
      this.inputHour = this.selectedDate.getHours();
      this.inputMinute = this.selectedDate.getMinutes();

      this.mv = this.getMonthView(this.selectedDate.getFullYear(), this.selectedDate.getMonth());
      this.today = format(new Date(), 'YYYY-MM-dd');
      if (this.mv.year === this.selectedDate.getFullYear() &&
        this.mv.month === this.selectedDate.getMonth()) {
        this.selectedDay = this.selectedDate.getDate();
      } else {
        this.selectedDay = null;
      }

      this.change();
    }

    openDatetimePicker() {
      this.openPicker = true;
    }

    closeDatetimePicker() {
      this.openPicker = false;
    }

    updateDate(day) {
      this.selectedDate = new Date(this.mv.year,
        this.mv.month, day || this.selectedDate.getDate(), this.inputHour, this.inputMinute);
      this.showDate = format(this.selectedDate, this.dateFormat || 'YYYY-MM-DD HH:mm');
      this.selectedDay = this.selectedDate.getDate();
      let dateValue;
      if (this.currentDate) {
        if (this.currentDate && this.currentDate.constructor === 'Date') {
          dateValue = this.selectedDate;
        } else {
          dateValue = format(this.selectedDate, this.dateFormat);
        }
        this.currentDate = dateValue;
      }
    }

    setDate(day) {
      this.updateDate(day);
    }

    getMonthView(year, month) {
      let yr = year;
      let mth = month;
      if (month > 11) {
        yr += 1;
      } else if (month < 0) {
        yr -= 1;
      }
      mth = (month + 12) % 12;
      const firstDayOfMonth = new Date(yr, mth, 1);
      const lastDayOfMonth = new Date(yr, mth + 1, 0);
      const lastDayOfPreviousMonth = new Date(yr, mth, 0);
      const daysInMonth = lastDayOfMonth.getDate();
      const daysInLastMonth = lastDayOfPreviousMonth.getDate();
      const dayOfWeek = firstDayOfMonth.getDay();
      // Ensure there are always leading days to give context
      const leadingDays = ((dayOfWeek - this.calendar.firstDayOfWeek) + 7) % 7 || 7;
      let trailingDays = this.calendar.days.slice(0, (6 * 7) - (leadingDays + daysInMonth));
      if (trailingDays.length > 7) {
        trailingDays = trailingDays.slice(0, trailingDays.length - 7);
      }

      return {
        year: yr,
        month: mth,
        days: this.calendar.days.slice(0, daysInMonth),
        leadingDays: this.calendar.days
          .slice(-leadingDays - (31 - daysInLastMonth), daysInLastMonth),
        trailingDays,
      };
    }

    isDateSelectable(day, month, year) {
      const someday = new Date(`${day}/${month + 1}/${year}`);
      someday.setHours(0, 0, 0, 0);
      if (this.futureOnly) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return someday >= today;
      } else if (!isNaN(Date.parse(this.startDate)) && !isNaN(Date.parse(this.endDate))) {
        const startDate = new Date(this.startDate);
        const endDate = new Date(this.endDate);
        startDate.setHours(0, 0, 0, 0);
        endDate.setHours(0, 0, 0, 0);
        return startDate <= someday && someday <= endDate;
      } else if (!isNaN(Date.parse(this.startDate)) && isNaN(Date.parse(this.endDate))) {
        const startDate = new Date(this.startDate);
        startDate.setHours(0, 0, 0, 0);
        return startDate <= someday;
      } else if (isNaN(Date.parse(this.startDate)) && !isNaN(Date.parse(this.endDate))) {
        const endDate = new Date(this.endDate);
        endDate.setHours(0, 0, 0, 0);
        return someday <= endDate;
      }

      return true;
    }

    addMonth(amount) {
      this.mv = this.getMonthView(this.mv.year, this.mv.month + amount);
    }

    getTemplateString() {
      return `${this.mv.year}-${this.mv.month + 1}-${this.mv.day}`;
    }

    buildCalendar() {
      const formats = this.locale.DATETIME_FORMATS;
      const firstDayOfWeek = 0;
      return {
        days: [...new Array(31)].map((d, index) => index + 1),
        months: formats.MONTH
          .map((month, i) =>
            ({
              fullName: month,
              shortName: formats.SHORTMONTH[i],
            })),
        daysOfWeek: [...new Array(7)].map((val, index) => {
          const day = formats.DAY[(index + firstDayOfWeek) % 7];

          return {
            fullName: day,
            firstLetter: day.substr(0, 1),
          };
        }),
        firstDayOfWeek: 0,
      };
    }

    change() {
      this.closeDatetimePicker();
      this.onChange({ $event: { value: format(this.selectedDate, this.dateFormat || 'YYYY-MM-DDTHH:mm') } });
    }
  },
};

export default DatePickerComponent;
