from System import Dram, Hm, DvfsDram, DvfsHm, System


def get_system(policy_num: int) -> System:
    if policy_num == 1:
        return Dram()
    elif policy_num == 2:
        return Hm()
    elif policy_num == 3:
        return DvfsDram()
    elif policy_num == 4:
        return DvfsHm()


get_system(int(input("[1]DRAM, [2]HM. [3]DVFS_DRAM, [4]DVFS_HM : "))).run()


