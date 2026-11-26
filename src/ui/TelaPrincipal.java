package ui;

import modelo.*;
import servico.*;
import javax.swing.*;
import java.awt.*;
import java.time.LocalDate;

/** Tela Swing. ASSOCIAÇÃO com Biblioteca; DEPENDÊNCIA de Livro/Aluno/etc. (cria nos handlers). */
public class TelaPrincipal extends JFrame {
    private final Biblioteca biblioteca;
    private final DefaultListModel<Item> modeloItens = new DefaultListModel<>();
    private final DefaultListModel<Pessoa> modeloPessoas = new DefaultListModel<>();
    private final DefaultListModel<Emprestimo> modeloEmp = new DefaultListModel<>();
    private final JComboBox<Pessoa> cbPessoa = new JComboBox<>();
    private final JComboBox<Item> cbItem = new JComboBox<>();

    public TelaPrincipal(Biblioteca biblioteca) {
        super("Biblioteca Universitária");
        this.biblioteca = biblioteca;
        JTabbedPane abas = new JTabbedPane();
        abas.addTab("Acervo", abaAcervo());
        abas.addTab("Pessoas", abaPessoas());
        abas.addTab("Empréstimos", abaEmprestimos());
        add(abas);
        setSize(760, 420);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        atualizar();
    }

    private JPanel abaAcervo() {
        JComboBox<String> tipo = new JComboBox<>(new String[]{"Livro", "Revista", "DVD"});
        JTextField titulo = new JTextField(14), extra = new JTextField(10);
        JButton add = new JButton("Adicionar");
        add.addActionListener(e -> {
            try {
                String t = titulo.getText().trim(), x = extra.getText().trim();
                if (t.isEmpty() || x.isEmpty()) throw new IllegalArgumentException("Preencha todos os campos.");
                Item item;
                switch ((String) tipo.getSelectedItem()) {
                    case "Livro":   item = new Livro(t, x); break;
                    case "Revista": item = new Revista(t, Integer.parseInt(x)); break;
                    default:        item = new DVD(t, Integer.parseInt(x));
                }
                biblioteca.adicionar(item);
                titulo.setText(""); extra.setText("");
                atualizar();
            } catch (NumberFormatException ex) {
                aviso("Edição / duração deve ser um número.");
            } catch (IllegalArgumentException ex) {
                aviso(ex.getMessage());
            }
        });
        JPanel topo = new JPanel(new FlowLayout(FlowLayout.LEFT));
        topo.add(new JLabel("Tipo:")); topo.add(tipo);
        topo.add(new JLabel("Título:")); topo.add(titulo);
        topo.add(new JLabel("Autor / Edição / Minutos:")); topo.add(extra);
        topo.add(add);
        return painel(topo, new JList<>(modeloItens));
    }

    private JPanel abaPessoas() {
        JComboBox<String> tipo = new JComboBox<>(new String[]{"Aluno", "Professor"});
        JTextField nome = new JTextField(10), extra = new JTextField(8),
                   rua = new JTextField(10), cidade = new JTextField(8);
        JButton add = new JButton("Adicionar");
        add.addActionListener(e -> {
            String n = nome.getText().trim(), x = extra.getText().trim(),
                   r = rua.getText().trim(), c = cidade.getText().trim();
            if (n.isEmpty() || x.isEmpty() || r.isEmpty() || c.isEmpty()) { aviso("Preencha todos os campos."); return; }
            Pessoa p = "Aluno".equals(tipo.getSelectedItem())
                    ? new Aluno(n, x, r, c) : new Professor(n, x, r, c);
            biblioteca.adicionar(p);
            nome.setText(""); extra.setText(""); rua.setText(""); cidade.setText("");
            atualizar();
        });
        JPanel topo = new JPanel(new FlowLayout(FlowLayout.LEFT));
        topo.add(tipo);
        topo.add(new JLabel("Nome:")); topo.add(nome);
        topo.add(new JLabel("Matrícula / Depto:")); topo.add(extra);
        topo.add(new JLabel("Rua:")); topo.add(rua);
        topo.add(new JLabel("Cidade:")); topo.add(cidade);
        topo.add(add);
        return painel(topo, new JList<>(modeloPessoas));
    }

    private JPanel abaEmprestimos() {
        JList<Emprestimo> lista = new JList<>(modeloEmp);
        JSpinner dias = new JSpinner(new SpinnerNumberModel(0, 0, 365, 1));
        JButton emprestar = new JButton("Emprestar");
        JButton devolver = new JButton("Devolver");

        emprestar.addActionListener(e -> {
            try {
                biblioteca.emprestar((Pessoa) cbPessoa.getSelectedItem(),
                        (Item) cbItem.getSelectedItem(), LocalDate.now());
                atualizar();
            } catch (BibliotecaException ex) { aviso(ex.getMessage()); }
        });
        devolver.addActionListener(e -> {
            try {
                Emprestimo emp = lista.getSelectedValue();
                if (emp == null) throw new BibliotecaException("Selecione um empréstimo ativo.");
                LocalDate dataDevolucao = emp.getData().plusDays((Integer) dias.getValue());
                double multa = biblioteca.devolver(emp, dataDevolucao);
                atualizar();
                JOptionPane.showMessageDialog(this, String.format("Devolvido! Multa: R$ %.2f", multa));
            } catch (BibliotecaException ex) { aviso(ex.getMessage()); }
        });

        JPanel topo = new JPanel(new FlowLayout(FlowLayout.LEFT));
        topo.add(new JLabel("Pessoa:")); topo.add(cbPessoa);
        topo.add(new JLabel("Item:")); topo.add(cbItem);
        topo.add(emprestar);
        JPanel base = new JPanel(new FlowLayout(FlowLayout.LEFT));
        base.add(new JLabel("Devolver após (dias do empréstimo):")); base.add(dias); base.add(devolver);
        JPanel p = painel(topo, lista);
        p.add(base, BorderLayout.SOUTH);
        return p;
    }

    private JPanel painel(JPanel topo, JList<?> lista) {
        JPanel p = new JPanel(new BorderLayout());
        p.add(topo, BorderLayout.NORTH);
        p.add(new JScrollPane(lista), BorderLayout.CENTER);
        return p;
    }

    private void atualizar() {
        modeloItens.clear(); cbItem.removeAllItems();
        for (Item i : biblioteca.getItens()) { modeloItens.addElement(i); cbItem.addItem(i); }
        modeloPessoas.clear(); cbPessoa.removeAllItems();
        for (Pessoa p : biblioteca.getPessoas()) { modeloPessoas.addElement(p); cbPessoa.addItem(p); }
        modeloEmp.clear();
        for (Emprestimo e : biblioteca.ativos()) modeloEmp.addElement(e);
    }

    private void aviso(String msg) {
        JOptionPane.showMessageDialog(this, msg, "Aviso", JOptionPane.WARNING_MESSAGE);
    }
}
