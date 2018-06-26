function changeFiles(files, eventFile, scope) {
  if (files.length > 0) {
    files.splice(0, 1, eventFile);
  } else {
    files.push(eventFile);
  }

  scope.$apply();
}

export const FileUploaderDirective = () => ({
  restrict: 'A',
  link(scope, element) {
    element.on('drag dragstart dragend dragover dragenter dragleave drop', (e) => {
      e.preventDefault();
      e.stopPropagation();
    })
      .on('dragover dragenter', () => {
        element.addClass('is-dragover');
      })
      .on('dragleave dragend drop', () => {
        element.removeClass('is-dragover');
      })
      .on('drop', (e) => {
        changeFiles(scope.files, e.dataTransfer.files[0], scope);
/*         const file = e.dataTransfer.files[0];
        if (scope.files.length > 0) {
          scope.files.splice(0, 1, file);
        } else {
          scope.files.push(file);
        }
        scope.$apply(); */
      })
      .on('change', (event) => {
        changeFiles(scope.files, event.target.files[0], scope);
      });
  },
});

export default FileUploaderDirective;
