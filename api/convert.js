const formidable = require('formidable');
const { PDFDocument } = require('pdf-lib');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const form = formidable({ multiples: false });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'File upload failed' });
    }

    try {
      // Basic conversion logic
      // Note: Full PDF to Word conversion requires additional libraries
      // This is a placeholder that demonstrates the structure
      
      res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
      res.setHeader('Content-Disposition', 'attachment; filename=converted.docx');
      
      // TODO: Implement actual PDF to Word conversion
      // Libraries needed: pdf-parse, docx, mammoth
      
      res.status(200).send('Conversion feature coming soon');
      
    } catch (error) {
      res.status(500).json({ error: 'Conversion failed' });
    }
  });
};
