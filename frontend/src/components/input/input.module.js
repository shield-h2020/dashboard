import angular from 'angular';
import { InputComponent } from './input.component';
import { SearchInputComponent } from './search/search-input.component';
import { SelectComponent } from './select/select.component';
import { AreaInputComponent } from './areainput.component';
import { InputFocusDirective } from './inputfocus.directive';
import { ActionFeedbackDirective } from './actionfeedback.directive';
import { DatePickerComponent } from './date-picker/date-picker.component';

export const InputModule = angular.module('input', [])
  .component('snInput', InputComponent)
  .component('snSearch', SearchInputComponent)
  .component('snSelect', SelectComponent)
  .component('snAreaInput', AreaInputComponent)
  .component('snDatePicker', DatePickerComponent)
  .directive('focus', ['$timeout', InputFocusDirective])
  .directive('actionFeedback', ['$timeout', '$compile', '$interpolate', ActionFeedbackDirective])
  .name;

export default InputModule;
