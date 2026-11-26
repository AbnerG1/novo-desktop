package modelo;

/** Parte de Pessoa (COMPOSIÇÃO): só existe dentro de uma Pessoa. */
public class Endereco {
    private final String rua;
    private final String cidade;

    Endereco(String rua, String cidade) { this.rua = rua; this.cidade = cidade; }

    @Override public String toString() { return rua + ", " + cidade; }
}
