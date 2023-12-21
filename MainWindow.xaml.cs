using System;
using System.Windows;
using System.Collections.Generic;
using System.Windows.Controls;
using System.IO;
using Microsoft.Win32;

namespace MinidimSharp
{
    public partial class MainWindow : Window
    {
        // Holds an instance of the ExcelConfigurationManager to manage Excel operations.
        private ExcelConfigurationManager? _configManager;
        
        // Path to the default folder where configurations are saved/loaded.
        private string defaultFolderPath;

        public MainWindow()
        {
            InitializeComponent(); // Initializes the components defined in XAML.

            // Set up the default folder path for "Dimensioneringer" in the same directory as the application.
            defaultFolderPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Dimensioneringer");
            Directory.CreateDirectory(defaultFolderPath); // Ensure the folder exists.
        }

        // Initializes the main content area with the Category1 UserControl.
        public void InitializeMainContent()
        {
            Category1 category1 = new Category1();
            if (category1.NameTextBox != null && category1.UnitComboBox != null && category1.ValueTextBox != null)
            {
                MainContent.Content = category1;
                _configManager = new ExcelConfigurationManager(category1.NameTextBox, category1.UnitComboBox, category1.ValueTextBox);
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
            // Check if the current content is Category1 and get its configuration data.
            if (MainContent.Content is Category1 category1)
            {
                var configurationData = category1.GetConfigurationData();
                
                // Validate the data before saving.
                if (configurationData == null || configurationData.Count == 0)
                {
                    MessageBox.Show("No configuration data to save.", "Warning", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                // Create a SaveFileDialog and set its properties.
                SaveFileDialog saveFileDialog = new SaveFileDialog();
                saveFileDialog.Filter = "Excel files (*.xlsx)|*.xlsx";
                saveFileDialog.DefaultExt = "xlsx";
                saveFileDialog.AddExtension = true;

                // Show the SaveFileDialog and get the result.
                bool? result = saveFileDialog.ShowDialog();

                // If the user clicked OK, save the file.
                if (result == true)
                {
                    // Check if _configManager is not null before using it.
                    if (_configManager != null)
                    {
                        try
                        {
                            // Save the configuration data using ExcelConfigurationManager.
                            _configManager.SaveConfiguration(configurationData, saveFileDialog.FileName);
                            MessageBox.Show("Configuration saved successfully.", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
                        }
                        catch (Exception ex)
                        {
                            // Log the exception details and inform the user.
                            MessageBox.Show($"Failed to save configuration: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                        }
                    }
                    else
                    {
                        // Inform the user that saving could not be completed due to an uninitialized configuration manager.
                        MessageBox.Show("Configuration manager is not initialized. Unable to save the configuration.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
            }
            else
            {
                // Inform the user if no configuration data is available to save.
                MessageBox.Show("No configuration data available to save.", "Information", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void LoadFile_Click(object sender, RoutedEventArgs e)
        {
            // Create an OpenFileDialog and set its properties.
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Excel files (*.xlsx)|*.xlsx";

            // Show the OpenFileDialog and get the result.
            bool? result = openFileDialog.ShowDialog();

            // If the user clicked OK, load the file.
            if (result == true)
            {
                string filePath = openFileDialog.FileName;

                try
                {
                    // Check if _configManager is not null before using it.
                    if (_configManager != null)
                    {
                        // Load the configuration data using ExcelConfigurationManager.
                        var configurationData = _configManager.LoadConfiguration(filePath);
                        // Use the loaded configuration data as needed.
                        // For example, update the UI or process the data further.
                    }
                    else
                    {
                        // Inform the user that loading could not be completed due to an uninitialized configuration manager.
                        MessageBox.Show("Configuration manager is not initialized. Unable to load the configuration.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    }
                }
                catch (FileNotFoundException fnfEx)
                {
                    MessageBox.Show($"File not found: {fnfEx.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }
    }
}