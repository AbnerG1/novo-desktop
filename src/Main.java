import modelo.*;
import servico.Biblioteca;
import ui.TelaPrincipal;
import javax.swing.SwingUtilities;

public class Main {
    public static void main(String[] args) {
        Biblioteca b = new Biblioteca();
        b.adicionar(new Livro("Clean Code", "Robert Martin"));
        b.adicionar(new Revista("Superinteressante", 450));
        b.adicionar(new DVD("Matrix", 136));
        b.adicionar(new Aluno("Abner", "240000001", "Rua 1", "Brasília"));
        b.adicionar(new Professor("Ana Souza", "FCTE", "Rua 2", "Gama"));
        SwingUtilities.invokeLater(() -> new TelaPrincipal(b).setVisible(true));
    }
}
