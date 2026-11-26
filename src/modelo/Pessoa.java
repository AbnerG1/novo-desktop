package modelo;

/** Classe abstrata: base da HERANÇA de usuários. Compõe um Endereco. */
public abstract class Pessoa {
    private final String nome;
    private final Endereco endereco; // COMPOSIÇÃO: criado aqui dentro

    protected Pessoa(String nome, String rua, String cidade) {
        this.nome = nome;
        this.endereco = new Endereco(rua, cidade);
    }

    public String getNome() { return nome; }
    public Endereco getEndereco() { return endereco; }

    // POLIMORFISMO
    public abstract int limiteEmprestimos();
    public abstract String tipo();

    @Override public String toString() {
        return tipo() + ": " + nome + " - " + endereco + " (limite " + limiteEmprestimos() + ")";
    }
}
