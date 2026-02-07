// Always active
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class BookManager {
    private List<Book> books;
    private Scanner scanner;
    private int nextId;

    public BookManager() {
        books = new ArrayList<>();
        scanner = new Scanner(System.in);
        nextId = 1;
    }

    public void start() {
        while (true) {
            showMenu();
            int choice = getIntInput();
            switch (choice) {
                case 1:
                    addBook();
                    break;
                case 2:
                    showAllBooks();
                    break;
                case 3:
                    deleteBook();
                    break;
                case 4:
                    System.out.println("Exiting system");
                    return;
                default:
                    System.out.println("Invalid option, please re-enter");
            }
        }
    }

    private void showMenu() {
        System.out.println("\n=== Book Management System ===");
        System.out.println("1. Add Book");
        System.out.println("2. View Book List");
        System.out.println("3. Delete Book");
        System.out.println("4. Exit System");
        System.out.print("Please select an operation: ");
    }

    private void addBook() {
        System.out.print("Please enter the title: ");
        String title = scanner.nextLine();
        System.out.print("Please enter the author: ");
        String author = scanner.nextLine();
        
        Book book = new Book(nextId++, title, author);
        books.add(book);
        System.out.println("Book added successfully!");
    }

    private void showAllBooks() {
        if (books.isEmpty()) {
            System.out.println("No books available");
        } else {
            System.out.println("\nBook List:");
            for (Book book : books) {
                System.out.println(book);
            }
        }
    }

    private void deleteBook() {
        if (books.isEmpty()) {
            System.out.println("No books available to delete");
            return;
        }
        
        System.out.print("Please enter the ID of the book to delete: ");
        int id = getIntInput();
        
        boolean removed = books.removeIf(book -> book.getId() == id);
        if (removed) {
            System.out.println("Book deleted successfully!");
        } else {
            System.out.println("Book with specified ID not found");
        }
    }

    private int getIntInput() {
        while (true) {
            try {
                return Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.print("Please enter a valid number: ");
            }
        }
    }

    public static void main(String[] args) {
        new BookManager().start();
    }
}