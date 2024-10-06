package com.example.dndpdfparser

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.chaquo.python.PyException
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : AppCompatActivity() {
    private lateinit var resultTextView: TextView
    private lateinit var progressBar: ProgressBar
    private lateinit var recyclerView: RecyclerView
    private lateinit var resultsAdapter: ResultsAdapter
    private var selectedDir: Uri? = null

    companion object {
        private const val PICK_PDF_DIR = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        resultTextView = findViewById(R.id.resultTextView)
        progressBar = findViewById(R.id.progressBar)
        recyclerView = findViewById(R.id.recyclerView)

        resultsAdapter = ResultsAdapter()
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = resultsAdapter

        findViewById<Button>(R.id.selectDirButton).setOnClickListener {
            openDirectoryChooser()
        }

        findViewById<Button>(R.id.parsePdfButton).setOnClickListener {
            selectedDir?.let { uri ->
                parsePdfs(uri)
            } ?: run {
                resultTextView.text = "Please select a directory first."
            }
        }
    }

    private fun openDirectoryChooser() {
        val intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        startActivityForResult(intent, PICK_PDF_DIR)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == PICK_PDF_DIR && resultCode == Activity.RESULT_OK) {
            data?.data?.let { uri ->
                selectedDir = uri
                contentResolver.takePersistableUriPermission(uri, 
                    Intent.FLAG_GRANT_READ_URI_PERMISSION or 
                    Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                resultTextView.text = "Selected directory: ${uri.path}"
            }
        }
    }

    private fun parsePdfs(uri: Uri) {
        progressBar.visibility = View.VISIBLE
        resultTextView.text = "Parsing PDFs..."

        lifecycleScope.launch(Dispatchers.Default) {
            try {
                val python = Python.getInstance()
                val pythonModule = python.getModule("parse_pdfs")

                val result = pythonModule.callAttr("process_pdfs_in_directory", applicationContext, uri.toString()).toJava(List::class.java) as List<Map<String, Any>>

                withContext(Dispatchers.Main) {
                    progressBar.visibility = View.GONE
                    resultTextView.text = "Parsing complete. Showing results."
                    resultsAdapter.setResults(result)
                }
            } catch (e: PyException) {
                withContext(Dispatchers.Main) {
                    progressBar.visibility = View.GONE
                    resultTextView.text = "Error: ${e.message}"
                }
            }
        }
    }
}