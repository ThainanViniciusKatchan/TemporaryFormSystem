
class FomartDocumets:
    def format_cpf(cpf) -> str:
        cpf = cpf.replace('.', '').replace('-', '')
        CPFJunto = []
        for i in range(0, 1):
            CpfSeparado = {'Digito': (cpf[:3] + '.')}
            CPFJunto.append(CpfSeparado)
            CpfSeparado = {'Digito': cpf[3:6] + '.'}
            CPFJunto.append(CpfSeparado)
            CpfSeparado = {'Digito': cpf[6:9] + '-'}
            CPFJunto.append(CpfSeparado)
            CpfSeparado = {'Digito': (cpf[9:])}
            CPFJunto.append(CpfSeparado)

        CPF = ''
        for N in CPFJunto:
            for K, V in N.items():
                CPF += V
        return CPF

    def Format_RG(rg) -> str:
        rg = rg.replace('.', '').replace('-', '')
        RGSeparado = []
        for i in range(0, 1):
            RgSeparado = {'Digito': (rg[:2] + '.')}
            RGSeparado.append(RgSeparado)
            RgSeparado = {'Digito': rg[2:5] + '.'}
            RGSeparado.append(RgSeparado)
            RgSeparado = {'Digito': rg[5:8] + '-'}
            RGSeparado.append(RgSeparado)
            RgSeparado = {'Digito': (rg[8:])}
            RGSeparado.append(RgSeparado)

        RG = ''
        for N in RGSeparado:
            for K, V in N.items():
                RG += V
        return RG

    def Format_Tel(Tel) -> str:
        Tel = Tel.replace('(', '').replace(')', '').replace('-', '')
        TelefoneSeparado = []
        if len(Tel) == 11:
            for i in range(0, 1):
                TelFormt = {'Digito': (Tel[:0] + '(')}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[0:2] + ') '}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[2:7] + '-'}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[7:11]}
                TelefoneSeparado.append(TelFormt)

            Tel = ''
            for N in TelefoneSeparado:
                for K, V in N.items():
                    Tel += V
            return Tel
        elif len(Tel) == 10:
            for i in range(0, 1):
                TelFormt = {'Digito': (Tel[:0] + '(')}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[0:2] + ') '}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[2:6] + '-'}
                TelefoneSeparado.append(TelFormt)
                TelFormt = {'Digito': Tel[6:10]}
                TelefoneSeparado.append(TelFormt)

            Tel = ''
            for N in TelefoneSeparado:
                for K, V in N.items():
                    Tel += V
            return Tel

    def Format_Cep(Cep) -> str:
        Cep = Cep.replace('-', '')
        CepSeparado = []
        for i in range(0, 1):
            CepFormt = {'Digito': (Cep[0:5] + '-')}
            CepSeparado.append(CepFormt)
            CepFormt = {'Digito': (Cep[5:])}
            CepSeparado.append(CepFormt)

        Cep = ''
        for N in CepSeparado:
            for K, V in N.items():
                Cep += V
        return Cep


if __name__ == '__main__':
    pass
