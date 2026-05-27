import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.List;

public class IOStreamDemo {

    private static final String FILE_PATH = "io_demo_output.txt";

    public static void main(String[] args) {
        IOStreamDemo demo = new IOStreamDemo();

        demo.writeWithFileOutputStream("Hello, IO Stream!\n");
        demo.appendWithFileOutputStream("This is appended content.\n");
        demo.readWithFileInputStream();

        demo.writeWithBufferedWriter("Buffered Writer Line 1\nBuffered Writer Line 2\n");
        demo.readWithBufferedReader();

        demo.copyFile(FILE_PATH, "io_demo_copy.txt");

        demo.writeWithNIO("NIO Content Line 1\nNIO Content Line 2\n");
        demo.readWithNIO();

        demo.readFromConsole();
    }

    public void writeWithFileOutputStream(String content) {
        try (FileOutputStream fos = new FileOutputStream(FILE_PATH)) {
            fos.write(content.getBytes(StandardCharsets.UTF_8));
            System.out.println("[FileOutputStream] Write completed.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void appendWithFileOutputStream(String content) {
        try (FileOutputStream fos = new FileOutputStream(FILE_PATH, true)) {
            fos.write(content.getBytes(StandardCharsets.UTF_8));
            System.out.println("[FileOutputStream] Append completed.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readWithFileInputStream() {
        try (FileInputStream fis = new FileInputStream(FILE_PATH)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            System.out.println("[FileInputStream] Reading file:");
            while ((bytesRead = fis.read(buffer)) != -1) {
                System.out.print(new String(buffer, 0, bytesRead, StandardCharsets.UTF_8));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void writeWithBufferedWriter(String content) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_PATH, StandardCharsets.UTF_8))) {
            writer.write(content);
            System.out.println("[BufferedWriter] Write completed.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readWithBufferedReader() {
        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_PATH, StandardCharsets.UTF_8))) {
            String line;
            System.out.println("[BufferedReader] Reading file:");
            while ((line = reader.readLine()) != null) {
                System.out.println("  " + line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void copyFile(String source, String destination) {
        try (InputStream in = new BufferedInputStream(new FileInputStream(source));
             OutputStream out = new BufferedOutputStream(new FileOutputStream(destination))) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
                out.write(buffer, 0, bytesRead);
            }
            System.out.println("[FileCopy] Copied " + source + " -> " + destination);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void writeWithNIO(String content) {
        try {
            Files.writeString(Path.of(FILE_PATH), content, StandardCharsets.UTF_8);
            System.out.println("[NIO Files] Write completed.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readWithNIO() {
        try {
            List<String> lines = Files.readAllLines(Path.of(FILE_PATH), StandardCharsets.UTF_8);
            System.out.println("[NIO Files] Reading file:");
            lines.forEach(line -> System.out.println("  " + line));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readFromConsole() {
        System.out.println("[Console] Enter a line of text (or press Enter to skip):");
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8))) {
            String input = reader.readLine();
            if (input != null && !input.isEmpty()) {
                System.out.println("[Console] You entered: " + input);
            } else {
                System.out.println("[Console] No input received, skipping.");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
