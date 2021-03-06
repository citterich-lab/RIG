import numpy as np


def _subscore(a, b, matrix, alpha_dict, gap_penalty=-2):
    """
    matrix is a dataframe with the substitution matrix, alphabet is the string of ordered alphabet characters
    """

    if a == '-' or b == '-':
        return gap_penalty

    return float(matrix.iat[alpha_dict[a], alpha_dict[b]])


def buildPSSM_alphabet(targets, matrix, gaps=True):
    """targets shall be in the form of a double-listed list [[seqs],[bears]]
    matrix is a dataframe
    PSSM built ala Citterich
    """

    alpha = "".join(matrix.index)
    if gaps:
        alpha += "-"
    alpha_dict = {x: i for i, x in enumerate(alpha)}

    w = len(targets[0][0])

    # initialize count matrix (alphabet X alignmentWidth)
    count = np.zeros((len(alpha), w), dtype=int)  # +NO PSEUDOCOUNT
    for i, _ in enumerate(targets[0][0]):
        for n, _ in enumerate(targets[0]):
            ch = targets[1][n][i]
            count[alpha_dict[ch]][i] += 1

    count = count / count.sum(axis=0)  ###RELATIVE FREQs

    pssm = np.zeros((len(alpha), w), dtype=float)  ## pseudocount in frequencies

    # multiply per subs mat
    for pos in np.arange(count.shape[1]):
        # print("building pos {}".format(pos))
        position_col = [c[pos] for c in count]
        ####TODO prende anche roba di altre posizioni
        # print(position_col)
        for idx, freq in enumerate(position_col):
            # print("filling character {}".format(BEAR[idx]))
            position_col_again = [
                _subscore(
                    alpha[idx], alpha[idx__], matrix, alpha_dict
                ) * freq__ for idx__, freq__ in enumerate(position_col)
            ]
            # print(position_col_again)
            pssm[idx][pos] = np.sum(position_col_again)

    return pssm


def buildPPM_alphabet(targets, matrix, gaps=True):
    alpha = "".join(matrix.index)
    if gaps:
        alpha += "-"
    alpha_dict = {x: i for i, x in enumerate(alpha)}

    w = len(targets[0][0])

    # initialize count matrix (alphabet X alignmentWidth)
    count = np.zeros((len(alpha), w), dtype=int)  # +NO PSEUDOCOUNT
    for i, _ in enumerate(targets[0][0]):
        for n, _ in enumerate(targets[0]):
            ch = targets[1][n][i]
            count[alpha_dict[ch]][i] += 1

    count = count / count.sum(axis=0)  ###RELATIVE FREQs
    return count


def buildPFM_alphabet(targets, matrix, gaps=True):
    alpha = "".join(matrix.index)
    if gaps: alpha += "-"
    w = len(targets[0][0])

    # initialize count matrix (alphabet X alignmentWidth)
    count = np.zeros((len(alpha), w), dtype=int)  # +NO PSEUDOCOUNT
    for i, _ in enumerate(targets[0][0]):
        for n, _ in enumerate(targets[0]):
            ch = targets[1][n][i]
            count[alpha.index(ch)][i] += 1

    return count
