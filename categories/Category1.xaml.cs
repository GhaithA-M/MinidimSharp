using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Collections.Generic;

namespace MinidimSharp
{
    public partial class Category1 : UserControl
    {

        public TextBox? NameTextBox { get; set; }
        public ComboBox? UnitComboBox { get; set; }
        public TextBox? ValueTextBox { get; set; }

        // Constructor initializes the user control and sets default values
        public Category1()
        {
            InitializeComponent(); // Initializes UI components from XAML
            VoltageTextBox.TextChanged += VoltageTextBox_TextChanged; // Subscribes to text changed event
            VoltageTextBox.Text = "230"; // Sets a default value for VoltageTextBox
        }

        // Provides public access to LoadEntriesPanel for other classes to interact with
        public UniformGrid LoadEntriesPanelPublic
        {
            get { return LoadEntriesPanel; }
        }

        // Collects and returns configuration data from UI elements as a dictionary
        public Dictionary<string, string> GetConfigurationData()
        {
            var data = new Dictionary<string, string>();

            // Assume there can be up to 20 entries
            for (int i = 0; i < 20; i++)
            {
                // Check if the entry exists
                if (LoadEntriesPanelPublic.Children.Count > i)
                {
                    var loadEntryPanel = LoadEntriesPanelPublic.Children[i] as StackPanel;
                    if (loadEntryPanel != null)
                    {
                        // Extract the controls from the loadEntryPanel
                        var nameTextBox = loadEntryPanel.Children[0] as TextBox;
                        var unitComboBox = loadEntryPanel.Children[1] as ComboBox;
                        var valueTextBox = loadEntryPanel.Children[2] as TextBox;

                        // Handles potential nulls and assigns default values if necessary
                        string name = nameTextBox?.Text ?? string.Empty;  // Empty string if null
                        string unit = unitComboBox?.SelectedItem?.ToString() ?? "[Unknown Unit]";  // Default unit if null
                        string value = valueTextBox?.Text ?? "0";  // Default to "0" if null

                        // Adds the data to the dictionary only if it's valid
                        if (!string.IsNullOrWhiteSpace(name) && !string.IsNullOrWhiteSpace(value))
                        {
                            string combinedValue = $"{unit} {value}";
                            data.Add(name, combinedValue);
                        }
                        else
                        {
                            // Optionally handle invalid data (e.g., log a warning or notify the user)
                        }
                    }
                }
            }
            return data;
        }

        // Event handler for VoltageTextBox's text changed event
        private void VoltageTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            // Attempts to parse the text as a double and calculates the new voltage
            if (double.TryParse(VoltageTextBox.Text, out var voltage))
            {
                var calculatedVoltage = voltage * Math.Sqrt(3); // Replace with the actual calculation
                CalculatedVoltageTextBox.Text = calculatedVoltage.ToString();
            }
            else
            {
                CalculatedVoltageTextBox.Text = "Ugyldig spænding."; // Displays an error message if parsing fails
            }
        }

        // Adds a new load entry to LoadEntriesPanel when the AddLoad button is clicked
        public void AddLoad_Click(object sender, RoutedEventArgs e)
        {
            if (LoadEntriesPanel.Children.Count < 20) // Limits the number of entries to 20
            {
                // Creates a new StackPanel for the load entry
                var loadEntryPanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 0, 0, 5) };

                // Adds a TextBox for the load's name
                var nameTextBox = new TextBox { Text = "Modstand " + (LoadEntriesPanel.Children.Count + 1) };
                loadEntryPanel.Children.Add(nameTextBox);

                // Adds a ComboBox for selecting the unit
                var unitComboBox = new ComboBox();
                unitComboBox.Items.Add("[A] Ampere");
                unitComboBox.Items.Add("[Ω] Ohm");
                unitComboBox.Items.Add("[W] Watt");
                unitComboBox.SelectedIndex = 1;  // Defaults to Ohm
                unitComboBox.Style = (Style)Resources["ComboBoxStyle"];
                loadEntryPanel.Children.Add(unitComboBox);

                // Adds a TextBox for the value of the load
                var valueTextBox = new TextBox { Width = 50 };
                valueTextBox.TextChanged += (s, e) => CalculateTotal();  // Recalculates total when value changes
                loadEntryPanel.Children.Add(valueTextBox);

                // Adds the new entry to LoadEntriesPanel and updates the counter
                LoadEntriesPanel.Children.Add(loadEntryPanel);
                CalculateTotal();  // Recalculates the total based on all entries
                LoadCounter.Content = $"{LoadEntriesPanel.Children.Count}/20";  // Updates the counter display
            }
        }

        // Removes the last load entry from LoadEntriesPanel when the RemoveLoad button is clicked
        private void RemoveLoad_Click(object sender, RoutedEventArgs e)
        {
            if (LoadEntriesPanel.Children.Count > 0)
            {
                LoadEntriesPanel.Children.RemoveAt(LoadEntriesPanel.Children.Count - 1);  // Removes the last entry
                LoadCounter.Content = $"{LoadEntriesPanel.Children.Count}/20";  // Updates the counter display
                CalculateTotal();
            }
        }

        // Calculates the total based on the entries and updates the Result TextBox
        public void CalculateTotal()
        {
            var total = 0.0;
            foreach (StackPanel loadEntryPanel in LoadEntriesPanel.Children)
            {
                var unitComboBox = (ComboBox)loadEntryPanel.Children[1];
                var valueTextBox = (TextBox)loadEntryPanel.Children[2];

                string valueText = valueTextBox?.Text ?? "0";
                string voltageText = VoltageTextBox?.Text ?? "230";  // Default voltage if null

                // Calculates the total based on the unit and value
                if (double.TryParse(valueText, out double value) && unitComboBox.SelectedItem != null)
                {
                    int selectedUnit = unitComboBox.SelectedIndex;
                    if (double.TryParse(voltageText, out double voltage))
                    {
                        // Switch based on the selected unit and perform appropriate calculation
                        switch (selectedUnit)
                        {
                            case 0: // Ampere | R = V / I
                                total += (value != 0) ? voltage / value : 0;  // Avoids division by zero
                                break;
                            case 1: // Ohm
                                total += value;
                                break;
                            case 2: // Watt | R = V^2 / P
                                total += (value != 0) ? Math.Pow(voltage, 2) / value : 0;  // Avoids division by zero
                                break;
                        }
                    }
                }
            }
            Result.Text = total.ToString();  // Updates the Result TextBox with the calculated total
        }

    }
}
