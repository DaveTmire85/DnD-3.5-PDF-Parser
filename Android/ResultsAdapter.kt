package com.example.dndpdfparser

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ResultsAdapter : RecyclerView.Adapter<ResultsAdapter.ViewHolder>() {
    private var results: List<Map<String, Any>> = emptyList()

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val titleTextView: TextView = view.findViewById(R.id.titleTextView)
        val contentTextView: TextView = view.findViewById(R.id.contentTextView)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.result_item, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val result = results[position]
        holder.titleTextView.text = result["title"] as? String ?: "Unknown"
        holder.contentTextView.text = result["content"] as? String ?: "No content"
    }

    override fun getItemCount() = results.size

    fun setResults(newResults: List<Map<String, Any>>) {
        results = newResults
        notifyDataSetChanged()
    }
}