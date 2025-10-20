import Button from "@/components/ui/Button";
import Modal from "@/components/ui/Modal";

export function EditBudgetModal({
  isOpen,
  onClose,
  data,
}: {
  isOpen: boolean;
  onClose: () => void;
  data: any;
}) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit Budget">
      {data && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            // call updateBudget API mutation
            onClose();
          }}
          className="flex flex-col space-y-4"
        >
          <input
            type="text"
            defaultValue={data.name}
            placeholder="Budget Name"
            className="border p-2 rounded w-full"
          />
          <input
            type="number"
            defaultValue={data.amount}
            placeholder="Amount"
            className="border p-2 rounded w-full"
          />
          <div className="flex justify-end space-x-2">
            <Button type="submit">Save</Button>
            <Button variant="secondary" onClick={onClose}>
              Cancel
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
