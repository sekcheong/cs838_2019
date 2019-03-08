using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Security;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace marker
{
    public partial class FormMain : Form
    {
        private string _fileName;
        public FormMain()
        {
            InitializeComponent();
        }

        private void SetText(string text)
        {
            textBox1.Clear();
            textBox1.Text = text;
        }

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            if (keyData == (Keys.Control | Keys.F)) {
                btnMark_Click(null,null);
                return true;
            }
            else if (keyData == (Keys.Control | Keys.S)) {
                btnSave_Click(null, null);
            }
            else if (keyData == (Keys.Control | Keys.R)) {
                btnOpen_Click(null, null);
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK) {
                try {
                    _fileName = openFileDialog1.FileName;
                    var sr = new StreamReader(_fileName);
                    SetText(sr.ReadToEnd());
                    this.Text = _fileName;
                    btnMark.Enabled = true;
                }
                catch (Exception ex) {
                    MessageBox.Show($"Error opening file.\n\nError message: {ex.Message}\n\n" + $"Details:\n\n{ex.StackTrace}");
                }
            }
        }

        private void btnMark_Click(object sender, EventArgs e)
        {            
            var txt = textBox1.Text;
            var tag = textBox2.Text;            
            string a = txt.Substring(0, textBox1.SelectionStart);
            string b = txt.Substring(textBox1.SelectionStart, textBox1.SelectionLength);
            string c = txt.Substring(textBox1.SelectionStart + textBox1.SelectionLength);

            if (b.StartsWith(" ")) {
                if (!a.EndsWith(" ")) a = a + " ";
            }

            if (b.EndsWith(" ")) {
                if (!c.StartsWith(" ")) c = " " + c;
            }

            textBox1.Text = a + "<" + tag + ">" + b.Trim() + "</" + tag + ">" + c;
            btnSave.Enabled = true;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            try {
                var fname = Path.GetFileName(_fileName);
                var path = Path.GetDirectoryName(_fileName);
                var p = path.Split(new char[] {'\\'});
                var cat = p[p.Length - 1];
                var filePath = Path.Combine(path, textBoxPrefix.Text+fname);
                var sr = new StreamWriter(filePath);
                var txt = textBox1.Text;                  
                sr.WriteLine(txt);
                sr.WriteLine("[" + cat +"][" + fname + "]");
                sr.Close();
            }
            catch (Exception ex) {
                MessageBox.Show($"Error opening saving file.\n\nError message: {ex.Message}\n\n" + $"Details:\n\n{ex.StackTrace}");
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            btnSave.Enabled = true;
        }
    }
}
