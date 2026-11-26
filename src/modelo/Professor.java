package modelo;

public class Professor extends Pessoa {
    private final String departamento;
    public Professor(String nome, String departamento, String rua, String cidade) {
        super(nome, rua, cidade);
        this.departamento = departamento;
    }
    @Override public int limiteEmprestimos() { return 5; }
    @Override public String tipo() { return "Professor " + departamento; }
}
