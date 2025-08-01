import { SELECTORS, CSS_CLASSES } from '../utils/constants.js';
import { FileValidator, FileFormatter, ValidationError } from '../utils/fileUtils.js';

export class FileUpload {
  constructor(onFileSelect, onError) {
    this.onFileSelect = onFileSelect;
    this.onError = onError;
    this.selectedFile = null;
    this.init();
  }

  init() {
    this.initializeElements();
    this.attachEventListeners();
  }

  initializeElements() {
    this.uploadArea = document.querySelector(SELECTORS.UPLOAD_AREA);
    this.fileInput = document.querySelector(SELECTORS.FILE_INPUT);
    this.selectedFileDiv = document.querySelector(SELECTORS.SELECTED_FILE);
    this.fileName = document.getElementById('fileName');
    this.fileSize = document.getElementById('fileSize');
    this.removeFileBtn = document.getElementById('removeFile');
    this.analyzeBtn = document.querySelector(SELECTORS.ANALYZE_BTN);
  }

  attachEventListeners() {
    // File input events
    this.uploadArea.addEventListener('click', () => this.fileInput.click());
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    this.removeFileBtn.addEventListener('click', () => this.removeFile());

    // Drag and drop events
    this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
    this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

    // Browse text click
    const browseText = document.querySelector('.browse-text');
    if (browseText) {
      browseText.addEventListener('click', (e) => {
        e.stopPropagation();
        this.fileInput.click();
      });
    }
  }

  handleDragOver(e) {
    e.preventDefault();
    this.uploadArea.classList.add(CSS_CLASSES.DRAGOVER);
  }

  handleDragLeave(e) {
    e.preventDefault();
    this.uploadArea.classList.remove(CSS_CLASSES.DRAGOVER);
  }

  handleDrop(e) {
    e.preventDefault();
    this.uploadArea.classList.remove(CSS_CLASSES.DRAGOVER);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      this.processFile(files[0]);
    }
  }

  handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
      this.processFile(file);
    }
  }

  processFile(file) {
    try {
      FileValidator.validate(file);
      this.selectedFile = file;
      this.displaySelectedFile(file);
      this.onFileSelect(file);
    } catch (error) {
      if (error instanceof ValidationError) {
        this.onError(error.message);
      } else {
        this.onError('An unexpected error occurred while processing the file.');
      }
    }
  }

  displaySelectedFile(file) {
    this.fileName.textContent = file.name;
    this.fileSize.textContent = FileFormatter.formatFileSize(file.size);

    this.uploadArea.style.display = 'none';
    this.selectedFileDiv.style.display = 'block';
    this.analyzeBtn.disabled = false;
  }

  removeFile() {
    this.selectedFile = null;
    this.fileInput.value = '';

    this.uploadArea.style.display = 'block';
    this.selectedFileDiv.style.display = 'none';
    this.analyzeBtn.disabled = true;
  }

  getSelectedFile() {
    return this.selectedFile;
  }

  reset() {
    this.removeFile();
  }
}