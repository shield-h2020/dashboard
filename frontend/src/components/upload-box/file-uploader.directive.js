export const FileUploader = () => ({
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
        const file = e.dataTransfer.files[0];
        if (scope.files.length > 0) {
          scope.files.splice(0, 1, file);
        } else {
          scope.files.push(file);
        }
        scope.$apply();
      });
  },
});

export default FileUploader;
