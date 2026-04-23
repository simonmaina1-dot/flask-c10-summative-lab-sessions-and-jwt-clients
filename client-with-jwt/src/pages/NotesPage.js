import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { Button } from "../styles";
import NoteList from "../components/NoteList";
import NewNoteForm from "../components/NewNoteForm";

function NotesPage() {
  const [notes, setNotes] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const token = localStorage.getItem("token");

  const loadNotes = async (pageNum = 1) => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/notes?page=${pageNum}&per_page=10`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        setNotes(data.notes);
        setPage(data.page);
        setTotalPages(data.pages);
      }
    } catch (error) {
      console.error("Error loading notes:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadNotes();
  }, []); // eslint-disable-next-line react-hooks/exhaustive-deps

  const handleNewNote = async (title, content) => {
    try {
      const response = await fetch("/api/notes", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, content }),
      });
      if (response.ok) {
        loadNotes(page);  // Reload current page
      }
    } catch (error) {
      console.error("Error creating note:", error);
    }
  };

  const handleUpdateNote = async (id, title, content) => {
    try {
      const response = await fetch(`/api/notes/${id}`, {
        method: "PATCH",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, content }),
      });
      if (response.ok) {
        loadNotes(page);
      }
    } catch (error) {
      console.error("Error updating note:", error);
    }
  };

  const handleDeleteNote = async (id) => {
    /* eslint-disable-next-line no-restricted-globals */
    if (!confirm("Are you sure you want to delete this note?")) return;
    try {
      const response = await fetch(`/api/notes/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      if (response.ok) {
        loadNotes(page);
      }
    } catch (error) {
      console.error("Error deleting note:", error);
    }
  };

  return (
    <Wrapper>
      <Header>
        <h1>Your Notes</h1>
        <Pagination>
          <Button 
            onClick={() => loadNotes(Math.max(1, page - 1))}
            disabled={page === 1 || isLoading}
          >
            Previous
          </Button>
          <span>Page {page} of {totalPages}</span>
          <Button 
            onClick={() => loadNotes(page + 1)}
            disabled={page === totalPages || isLoading}
          >
            Next
          </Button>
        </Pagination>
      </Header>
      
      <NewNoteForm onNewNote={handleNewNote} />
      
      {isLoading ? (
        <Loading>Loading notes...</Loading>
      ) : (
        <NoteList 
          notes={notes}
          onUpdate={handleUpdateNote}
          onDelete={handleDeleteNote}
        />
      )}
    </Wrapper>
  );
}

const Wrapper = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
`;

const Pagination = styled.div`
  display: flex;
  gap: 10px;
  align-items: center;
`;

const Loading = styled.div`
  text-align: center;
  padding: 40px;
  font-size: 1.2em;
`;

export default NotesPage;

