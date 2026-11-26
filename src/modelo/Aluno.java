package modelo;

public class Aluno extends Pessoa {
    private final String matricula;
    public Aluno(String nome, String matricula, String rua, String cidade) {
        super(nome, rua, cidade);
        this.matricula = matricula;
    }
    @Override public int limiteEmprestimos() { return 3; }
    @Override public String tipo() { return "Aluno " + matricula; }
}
