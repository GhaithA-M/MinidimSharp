using System;
using System.Windows;
using System.Collections.Generic;
using System.Windows.Controls;
using System.IO;
using Microsoft.Win32;
using OfficeOpenXml;

namespace MinidimSharp
{
    public partial class MainWindow : Window
    {
        // Path to the default folder where configurations are saved/loaded.
        private string defaultFolderPath;
        private Category1 category1;

        public MainWindow()
        {
            InitializeComponent(); // Initializes the components defined in XAML.
            // Set up the default folder path for "Dimensioneringer" in the same directory as the application.
            defaultFolderPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Dimensioneringer");
            Directory.CreateDirectory(defaultFolderPath); // Ensure the folder exists.
            InitializeMainContent();
        }

        // Initializes the main content area with the Category1 UserControl.
        public void InitializeMainContent()
        {
            category1 = new Category1();
            if (category1.NameTextBox != null && category1.UnitComboBox != null && category1.ValueTextBox != null)
            {
                MainContent.Content = category1;
            }
            else
            {
                // Handle the case where the controls are null.
                // You might want to show an error message to the user or throw an exception.
            }
        }

        // Placeholder for logic to handle creating a new file.
        private void NewFile_Click(object sender, RoutedEventArgs e)
        {
            // Implement the logic for creating a new file.
        }

          private void SaveAsFile_Click(object sender, RoutedEventArgs e)
        {
            // Assuming you have a reference to the Category1 instance
            Dictionary<string, string> inputData = category1.GetConfigurationData();

            using (ExcelPackage ExcelPkg = new ExcelPackage())
            {
                ExcelWorksheet wsSheet1 = ExcelPkg.Workbook.Worksheets.Add("Sheet1");

                int row = 1;
                foreach (KeyValuePair<string, string> entry in inputData)
                {
                    wsSheet1.Cells[row, 1].Value = entry.Key;
                    wsSheet1.Cells[row, 2].Value = entry.Value;
                    row++;
                }

                wsSheet1.Protection.IsProtected = false;
                wsSheet1.Protection.AllowSelectLockedCells = false;

                // Prompt the user to select a location to save the file
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "Excel files (*.xlsx)|*.xlsx";

                if (saveFileDialog.ShowDialog() == true)
                {
                    ExcelPkg.SaveAs(new FileInfo(saveFileDialog.FileName));
                }
            }
        }

        private void LoadFile_Click(object sender, RoutedEventArgs e)
        {
            // Implement the logic for loading a file.
        }

        private void MenuItem_Click(object sender, RoutedEventArgs e)
        {

        }
    }
}