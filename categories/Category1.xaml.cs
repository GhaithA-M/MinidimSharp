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
            var loadEntryPanel = new StackPanel { Orientation = Orientation.Horizontal };

            var unitComboBox = new ComboBox();
            unitComboBox.Items.Add("Amps");
            unitComboBox.Items.Add("Ohms");
            unitComboBox.Items.Add("Watts");
            unitComboBox.SelectedIndex = 0; // Default to Amps

            var valueTextBox = new TextBox { Width = 100 };

            loadEntryPanel.Children.Add(unitComboBox);
            loadEntryPanel.Children.Add(valueTextBox);

            LoadEntriesPanel.Children.Add(loadEntryPanel);
        }
    }
}
