using System;
using System.Windows;
using System.Windows.Controls;

namespace MinidimSharp
{
    public partial class Category1 : UserControl
    {
        public Category1()
        {
            InitializeComponent();
        }

        private void AddLoad_Click(object sender, RoutedEventArgs e)
        {
            var loadEntryPanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 0, 0, 5) };

            var nameTextBox = new TextBox { Text = "Belastning " + (LoadEntriesPanel.Children.Count + 1) };
            loadEntryPanel.Children.Add(nameTextBox);

            var unitComboBox = new ComboBox();
            unitComboBox.Items.Add("[A] Ampere");
            unitComboBox.Items.Add("[Ω] Ohm");
            unitComboBox.Items.Add("[W] Watt");
            unitComboBox.SelectedIndex = 0; // Default to Amps

            var valueTextBox = new TextBox { Width = 100 };

            loadEntryPanel.Children.Add(unitComboBox);
            loadEntryPanel.Children.Add(valueTextBox);

            LoadEntriesPanel.Children.Add(loadEntryPanel);

            CalculateTotal(); // Call CalculateTotal method after adding the load entry
        }

        // Add all inputs values together and display the result
        private void Calculate_Click(object sender, RoutedEventArgs e)
        {
            CalculateTotal();
        }

        private void CalculateTotal()
        {
            var total = 0.0;

            foreach (StackPanel loadEntryPanel in LoadEntriesPanel.Children)
            {
                var unitComboBox = (ComboBox)loadEntryPanel.Children[1];
                var valueTextBox = (TextBox)loadEntryPanel.Children[2];

                if (double.TryParse(valueTextBox.Text, out var value))
                {
                    switch (unitComboBox.SelectedIndex)
                    {
                        case 0: // Ampere
                            total += value;
                            break;
                        case 1: // Ohm
                            total += 1 / value;
                            break;
                        case 2: // Watt
                            total += Math.Sqrt(value);
                            break;
                    }
                }
            }

            Result.Text = total.ToString();
        }
    }
}
