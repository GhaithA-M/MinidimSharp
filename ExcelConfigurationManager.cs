using System;
using System.Collections.Generic;
using System.IO;
using OfficeOpenXml;
using Microsoft.Win32;
using System.Windows.Controls; // Needed for TextBox and ComboBox

public class ExcelConfigurationManager
{
    // Assuming these are your TextBox and ComboBox controls.
    TextBox nameTextBox;
    ComboBox unitComboBox;
    TextBox valueTextBox;

    public ExcelConfigurationManager(TextBox nameTextBox, ComboBox unitComboBox, TextBox valueTextBox)
    {
        this.nameTextBox = nameTextBox ?? throw new ArgumentNullException(nameof(nameTextBox));
        this.unitComboBox = unitComboBox ?? throw new ArgumentNullException(nameof(unitComboBox));
        this.valueTextBox = valueTextBox ?? throw new ArgumentNullException(nameof(valueTextBox));
    }

    public void SaveButton_Click(object sender, System.EventArgs e)
    {
        // Get the user inputs from the controls.
        string name = nameTextBox.Text;
        string unit = unitComboBox.SelectedItem?.ToString() ?? "DefaultUnit";
        string value = valueTextBox.Text;

        // Create a dictionary with the user inputs.
        var configurationData = new Dictionary<string, string>
        {
            { "Name", name },
            { "Unit", unit },
            { "Value", value }
        };

        // Save the configuration data to an Excel file.
        SaveConfiguration(configurationData, "Dimensioneringer.xlsx");
    }

    public void LoadButton_Click(object sender, System.EventArgs e)
    {
        // Open a OpenFileDialog to select the Excel file.
        OpenFileDialog openFileDialog = new OpenFileDialog();
        openFileDialog.Filter = "Excel files (*.xlsx)|*.xlsx";
        openFileDialog.DefaultExt = "xlsx";
        bool? result = openFileDialog.ShowDialog();

        // If the user clicked OK, load the file.
        if (result == true)
        {
            string filePath = openFileDialog.FileName;

            // Load the configuration data from the Excel file.
            var configurationData = LoadConfiguration(filePath);

            // Display the loaded data in the controls.
            nameTextBox.Text = configurationData["Name"];
            unitComboBox.SelectedItem = configurationData["Unit"];
            valueTextBox.Text = configurationData["Value"];
        }
    }

    public void SaveConfiguration(Dictionary<string, string> configurationData, string filePath)
    {
        using (var package = new ExcelPackage(new FileInfo(filePath)))
        {
            var worksheet = package.Workbook.Worksheets.Add("Sheet1");

            int row = 1;
            foreach (var pair in configurationData)
            {
                worksheet.Cells[row, 1].Value = pair.Key;
                worksheet.Cells[row, 2].Value = pair.Value;
                row++;
            }

            package.Save();
        }
    }

    public Dictionary<string, string> LoadConfiguration(string filePath)
    {
        var data = new Dictionary<string, string>();

        // Check if the file exists.
        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException("The specified file was not found.", filePath);
        }

        // Load the Excel package.
        using (var package = new ExcelPackage(new FileInfo(filePath)))
        {
            // Assume data is in the first worksheet.
            var worksheet = package.Workbook.Worksheets[0];
            if (worksheet == null)
            {
                throw new Exception("The worksheet could not be found.");
            }

            // Calculate the range of data (assuming data starts at row 2).
            int startRow = 2;
            int totalRows = worksheet.Dimension.End.Row;

            // Loop through rows and add data to the dictionary.
            for (int row = startRow; row <= totalRows; row++)
            {
                string key = worksheet.Cells[row, 1].Text;
                string value = worksheet.Cells[row, 2].Text;

                // Add key-value pair to the dictionary, handling potential duplicates or nulls as needed.
                if (!string.IsNullOrWhiteSpace(key) && !data.ContainsKey(key) && value != null)
                {
                    data.Add(key, value);
                }
            }
        }

        return data;
    }

}