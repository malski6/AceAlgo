function createFormFromSheet() {
  // Replace this with your Google Sheet ID
  const SHEET_ID = 'Your FormID here';
  
  // Get the sheet data
  const sheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  // Create a new form
  const form = FormApp.create('Survey Form');
  
  // Skip header row and process each row
  let currentSection = '';
  let sectionObject = null;
  
  // Process each row starting from index 1 (skipping header)
  for (let i = 1; i < data.length; i++) {
    const row = {
      QuestionTitle: data[i][0],
      QuestionType: data[i][1],
      Options: data[i][2],
      Section: data[i][3],
      Required: data[i][4],
      Other: data[i][5]
    };
    
    // Check if we need to create a new section
    if (row.Section !== currentSection) {
      currentSection = row.Section;
      sectionObject = form.addPageBreakItem().setTitle(currentSection);
    }
    
    // Create question based on type
    let questionItem;
    
    switch(row.QuestionType.toLowerCase()) {
      case "text":
        questionItem = form.addTextItem();
        break;
        
      case "paragraph":
        questionItem = form.addParagraphTextItem();
        break;
        
      case "dropdown":
        questionItem = form.addListItem();
        const dropdownOptions = row.Options.split(',')
          .map(opt => opt.trim())
          .filter(opt => opt !== '');
          
        if (row.Other === true || row.Other === "TRUE") {
          dropdownOptions.push("Other");
        }
        
        questionItem.setChoiceValues(dropdownOptions);
        break;

      case "scale":
        questionItem = form.addScaleItem();
        const [min, max] = row.Options.split(',').map(num => parseInt(num.trim()));
        questionItem.setBounds(min || 1, max || 5);
        break;

      case "checkbox":
        questionItem = form.addCheckboxItem();
        const checkboxOptions = row.Options.split(',')
          .map(opt => opt.trim())
          .filter(opt => opt !== '');
          
        if (row.Other === true || row.Other === "TRUE") {
          checkboxOptions.push("Other");
        }
        
        questionItem.setChoiceValues(checkboxOptions);
        break;

      case "file":
        questionItem = form.addFileUploadItem();
        // Optional: Configure file upload settings
        questionItem.setAllowFileUploads(true);
        break;

      case "multiple choice grid":
        questionItem = form.addGridItem();
        const [rowOptions, colOptions] = row.Options.split(';')
          .map(options => options.split(',')
            .map(opt => opt.trim())
            .filter(opt => opt !== '')
          );
        questionItem.setRows(rowOptions).setColumns(colOptions);
        break;

      case "checkbox grid":
        questionItem = form.addCheckboxGridItem();
        const [checkboxRows, checkboxCols] = row.Options.split(';')
          .map(options => options.split(',')
            .map(opt => opt.trim())
            .filter(opt => opt !== '')
          );
        questionItem.setRows(checkboxRows).setColumns(checkboxCols);
        break;

      case "date":
        questionItem = form.addDateItem();
        // Optional: Include year and show month/day in separate text boxes
        questionItem.setIncludesYear(true);
        break;

      case "time":
        questionItem = form.addTimeItem();
        break;
    }
    
    // Set question title and required status
    if (questionItem) {
      questionItem.setTitle(row.QuestionTitle);
      questionItem.setRequired(row.Required === true || row.Required === "TRUE");
    }
  }
  
  // Set form settings
  form.setCollectEmail(true)
    .setProgressBar(true)
    .setShowLinkToRespondAgain(false)
    .setConfirmationMessage('Thank you for your response!')
    .setAllowResponseEdits(false);
    
  // Log the URLs
  Logger.log('Form URL: ' + form.getPublishedUrl());
  Logger.log('Form edit URL: ' + form.getEditUrl());
  
  // Return to the spreadsheet and add the form URLs
  const urlSheet = SpreadsheetApp.openById(SHEET_ID).getActiveSheet();
  urlSheet.getRange('H1').setValue('Form URL');
  urlSheet.getRange('H2').setValue(form.getPublishedUrl());
  urlSheet.getRange('I1').setValue('Edit URL');
  urlSheet.getRange('I2').setValue(form.getEditUrl());
}
